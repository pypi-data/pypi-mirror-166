#!/usr/bin/env python
# encoding: utf-8

import os
import numpy as np
import math
from scipy.stats import ks_2samp
from matplotlib import pyplot as plt
import pandas as pd
import sys
import argparse
import seaborn as sns
from sklearn.svm import l1_min_c
from sympy import beta
from torch import alpha_dropout
from tvgl import *
from load_data import *
import matplotlib
import torch

sys.path.insert(1, './mmdagg/')
from tests import *

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

sys.path.insert(1, 'other_methods/klcpd')
from model import *

sys.path.insert(1, 'other_methods/graphtime')
from graphtime import GroupFusedGraphLasso
from utils import get_change_points, plot_data_with_cps

# KS-Test with Bonferroni Correction Change Point Detection
class KSTB_CPD():
    def __init__(self, series:np.array, p_wnd_dim:int=25, f_wnd_dim:int=25, threshold:int=.05):
        """
        @param series - timeseries
        @param p_wnd_dim - past window size
        @param f_wnd_dim - future window size
        @param threshold - threshold for dynamic windowing
        """
        super().__init__()
        self.p_wnd_dim = p_wnd_dim
        self.f_wnd_dim = f_wnd_dim
        self.series = series
        self.threshold = threshold
        #t_vals:
        self.scores = self.dynamic_windowing(self.p_wnd_dim, self.f_wnd_dim, self.series, self.threshold)
                
    def univariate_ks(self, prev, next):
        """
        Univariate 2 Sample Testing with Bonferroni Aggregation

        Arguments:
            prev {vector} -- [n_sample1, dim]
            next {vector} -- [n_sample2, dim]
        Returns:
            p_val -- [p-value]
            t_val -- [t-value, i.e. KS test-statistic]

        """
        p_vals = []
        t_vals = []

        # for each dimension, we conduct a separate KS test
        for i in range(prev.shape[1]):
            feature_tr = prev[:, i]
            feature_te = next[:, i]

            t_val, p_val = None, None
            t_val, p_val = ks_2samp(feature_tr, feature_te)
            p_vals.append(p_val)
            t_vals.append(t_val)

        # apply the Bonferroni correction for the family-wise error rate by picking the minimum
        # p-value from all individual tests
        p_vals = np.array(p_vals)
        t_vals = np.array(t_vals)
        p_val = min(np.min(p_vals), 1.0)
        t_val = np.mean(t_vals)
  
        return p_val, t_val
    
    def dynamic_windowing(self, p_wnd_dim, f_wnd_dim, series, threshold):

        t_vals = np.asarray([])
        p_vals = np.asarray([])

        run_length = int(p_wnd_dim)
        i = p_wnd_dim

        while i < len(series):
            prev = series[max(int(i)-run_length,0):int(i), :]
            next = series[max(int(i),0):int(i)+f_wnd_dim, :]

            if next.shape[0]<=2 or prev.shape[0]<=2:
                break

            p_val, t_val = self.univariate_ks(prev, next)

            if p_val >= threshold:
                t_vals = np.concatenate((t_vals, np.repeat(t_val, 1)))
                t_vals = np.concatenate((t_vals, np.repeat(0, f_wnd_dim-1)))
                i += f_wnd_dim
                run_length += p_wnd_dim
            else:
                t_vals = np.concatenate((t_vals, np.repeat(t_val, 1)))
                i+=1
                run_length = p_wnd_dim

        t_vals= np.concatenate((np.zeros(int((series.shape[0]-np.asarray(t_vals).shape[0]))),
                         np.asarray(t_vals)))

        return t_vals

    def visualize_results(self, series, t_vals, gt_cov, gt_mean, gt_var, label):

        f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(series)
        ax1.plot(gt_cov, label = 'gt_cov')
        ax1.plot(gt_mean, label = 'gt_mean')
        ax1.plot(gt_var, label = 'gt_var')
        ax1.legend(loc="upper right")

        ax2.plot(t_vals, label = label)
        ax2.legend(loc="upper right")

        return plt

# KS-Test with Bonferroni Correction Change Point Detection and Time Varying GL
class KSTBTVGL_CPD():
    def __init__(self, series:np.array, p_wnd_dim:int=25, f_wnd_dim:int=25, threshold:int=.2, alpha:int=5, beta:int=10,
                                            penalty_type='L1', slice_size:int=10, overlap:int=1, max_iters:int=1500):
        """
        @param series - timeseries
        @param p_wnd_dim - past window size
        @param f_wnd_dim - future window size
        @param threshold - threshold for dynamic windowing
        @param alpha - default, 5
        @param beta - default, 10
        @param penalty_type - 'L1' or 'L2'
        @param slice_size - default, 10
        @param overlap - measure of granularity, default=1
        @param max_iters - maximum number of iterations, default=1500
        """
        super().__init__()
        self.p_wnd_dim = p_wnd_dim
        self.f_wnd_dim = f_wnd_dim
        self.series = series
        self.threshold = threshold
        self.alpha = alpha
        self.beta = beta
        self.penalty_type = penalty_type
        self.slice_size = slice_size
        self.overlap = overlap
        self.max_iters = max_iters

        self.t_vals = self.dynamic_windowing(self.p_wnd_dim, self.f_wnd_dim, self.series, self.threshold)
        self.corr_score = self.TVGL_(series=self.series, alpha = self.alpha, beta =self.beta, penalty_type=self.penalty_type,
                                            slice_size=self.slice_size, overlap=self.overlap, threshold=self.threshold, max_iters=self.max_iters)

        self.scores = self.t_vals+ abs(self.corr_score)

                
    def univariate_ks(self, prev, next):
        """
        Univariate 2 Sample Testing with Bonferroni Aggregation

        Arguments:
            prev {vector} -- [n_sample1, dim]
            next {vector} -- [n_sample2, dim]
        Returns:
            p_val -- [p-value]
            t_val -- [t-value, i.e. KS test-statistic]

        """
        p_vals = []
        t_vals = []

        # for each dimension, we conduct a separate KS test
        for i in range(prev.shape[1]):
            feature_tr = prev[:, i]
            feature_te = next[:, i]

            t_val, p_val = None, None
            t_val, p_val = ks_2samp(feature_tr, feature_te)
            p_vals.append(p_val)
            t_vals.append(t_val)

        # apply the Bonferroni correction for the family-wise error rate by picking the minimum
        # p-value from all individual tests
        p_vals = np.array(p_vals)
        t_vals = np.array(t_vals)
        p_val = min(np.min(p_vals), 1.0)
        t_val = np.mean(t_vals)
  
        return p_val, t_val
    
    def dynamic_windowing(self, p_wnd_dim, f_wnd_dim, series, threshold):

        t_vals = np.asarray([])
        p_vals = np.asarray([])

        run_length = int(p_wnd_dim)
        i = p_wnd_dim

        while i < len(series):
            prev = series[max(int(i)-run_length,0):int(i), :]
            next = series[max(int(i),0):int(i)+f_wnd_dim, :]

            if next.shape[0]<=2 or prev.shape[0]<=2:
                break

            p_val, t_val = self.univariate_ks(prev, next)

            if p_val >= threshold:
                t_vals = np.concatenate((t_vals, np.repeat(t_val, 1)))
                t_vals = np.concatenate((t_vals, np.repeat(0, f_wnd_dim-1)))
                i += f_wnd_dim
                run_length += p_wnd_dim
            else:
                t_vals = np.concatenate((t_vals, np.repeat(t_val, 1)))
                i+=1
                run_length = p_wnd_dim

        t_vals= np.concatenate((np.zeros(int((series.shape[0]-np.asarray(t_vals).shape[0]))),
                         np.asarray(t_vals)))

        

        return t_vals

    def visualize_results(self, series, t_vals, gt_cov, gt_mean, gt_var, label):

        f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(series)
        ax1.plot(gt_cov, label = 'gt_cov')
        ax1.plot(gt_mean, label = 'gt_mean')
        ax1.plot(gt_var, label = 'gt_var')
        ax1.legend(loc="upper right")

        ax2.plot(t_vals, label = label)
        ax2.legend(loc="upper right")

        return plt

    def correlation_from_covariance(self, covariance):
        v = np.sqrt(np.diag(covariance))
        outer_v = np.outer(v, v)
        correlation = covariance / outer_v
        correlation[covariance == 0] = 0
        return correlation

    def shift(self, arr, shift):
        r_arr = np.roll(arr, shift=shift)
        m_arr = ma.masked_array(r_arr,dtype=float)
        if shift > 0: m_arr[:shift] = ma.masked
        else: m_arr[shift:] = ma.masked
        return m_arr.filled(0)
    
    def TVGL_(self, series, alpha, beta, penalty_type, slice_size, overlap, threshold, max_iters):
        
        model = TVGL(alpha, beta, penalty_type, slice_size, overlap=overlap, max_iters=max_iters)

        model.fit(series)
        # set of precision matrice
        
        ps = model.precision_set
    
        corr_score = np.asarray([])

        for i in range(len(ps)):
            #x = ((ps[i])-(ps[i-1]))
            x = self.correlation_from_covariance(np.linalg.inv(ps[i]))- self.correlation_from_covariance(np.linalg.inv(ps[i-1]))
            #x = (numpy.linalg.inv(ps[i]))- (numpy.linalg.inv(ps[i-1]))
            max_x = max(x.min(), x.max(), key=abs)
            if abs(max_x) < 0:
                max_x = 0
            corr_score=np.concatenate((corr_score, np.repeat(max_x, 1)))
            corr_score=np.concatenate((corr_score, np.repeat(0, overlap-1)))

        if len(corr_score) > len(series):
            corr_score=corr_score[:len(series)]
        else:
            corr_score=np.concatenate((corr_score,np.zeros(int(series.shape[0]-len(corr_score)))))

        return corr_score

# MMD Aggregate Change Point Detection
class MMDA_CPD():
    def __init__(self, series:np.array, p_wnd_dim:int=3, f_wnd_dim:int=3, threshold:int=.2, alpha:int=.001,
    kernel_type='laplace', approx_type='permutation', B1:int=500, B2:int=500, B3:int=100, weights_type='uniform', l_minus:int=0, l_plus:int=4):
        """
        @param series - timeseries
        @param p_wnd_dim - past window size
        @param f_wnd_dim - future window size
        @param threshold - threshold for dynamic windowing
        @param alpha - real number in (0,1) (level of the test)
        @param kernel_type - "gaussian" or "laplace"
        @param approx_type - "permutation" (for MMD_a estimate Eq. (3)) or "wild bootstrap" (for MMD_b estimate Eq. (6))
        @param B1 - number of simulated test statistics to estimate the quantiles
        @param B2 - number of simulated test statistics to estimate the probability in Eq. (13) in our paper
        @param B3 - number of iterations for the bisection method output: result of MMDAgg (1 for "REJECT H_0" and 0 for "FAIL TO REJECT H_0")
        @param weights_type 
        @param l_minus - lower value in bandwidth search range
        @param l_plus - upper value in bandwidth search range
        """
        super().__init__()
        self.p_wnd_dim = p_wnd_dim
        self.f_wnd_dim = f_wnd_dim
        self.series = series
        self.threshold = threshold
        self.alpha = alpha
        self.kernel_type = kernel_type
        self.approx_type = approx_type
        self.B1 = B1
        self.B2 = B2
        self.B3 = B3
        self.weights_type=weights_type
        self.l_minus=l_minus
        self.l_plus=l_plus

        self.scores = self.dynamic_windowing(p_wnd_dim, f_wnd_dim, series, threshold, alpha, kernel_type, 
                                                    approx_type, B1, B2, B3, weights_type, l_minus, l_plus)

    def dynamic_windowing(self, p_wnd_dim, f_wnd_dim, series, threshold, alpha, kernel_type,approx_type, B1, B2, B3, weight_type, l_minus, l_plus):

        mmd_agg = np.asarray([])

        run_length = int(p_wnd_dim)
        i = p_wnd_dim

        while i <= len(series):
            prev = series[max(int(i)-run_length,0):int(i), :]
            next = series[max(int(i),0):int(i)+f_wnd_dim, :]

            if next.shape[0]<=2 or prev.shape[0]<=2:
                break

            hyp = mmdagg(123, prev, next, alpha=alpha, kernel_type=kernel_type, approx_type=approx_type,weights_type=weight_type, l_minus=l_minus, l_plus=l_plus, 
            B1 = B1, B2 = B2, B3 = B3)
            
            if hyp >=threshold:
                mmd_agg = np.concatenate((mmd_agg, np.repeat(hyp, 1)))
                run_length = p_wnd_dim
                i+=1
            else:   
                mmd_agg = np.concatenate((mmd_agg, np.repeat(0, 1)))             
                mmd_agg = np.concatenate((mmd_agg, np.repeat(0, f_wnd_dim-1)))
                run_length += p_wnd_dim
                i += f_wnd_dim


        return np.concatenate((np.zeros(p_wnd_dim), mmd_agg))  

    def visualize_results(self, series, scores, gt_cov, gt_mean, gt_var, label):

        f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(series)
        ax1.plot(gt_cov, label = 'gt_cov')
        ax1.plot(gt_mean, label = 'gt_mean')
        ax1.plot(gt_var, label = 'gt_var')
        ax1.legend(loc="upper right")

        ax2.plot(scores, label = label)
        ax2.legend(loc="upper right")

        return plt


# MMD Aggregate Change Point Detection, Time Varying GL
class MMDATVGL_CPD():
    def __init__(self, series:np.array, p_wnd_dim:int=5, f_wnd_dim:int=10, threshold:int=.05, alpha:int=.05,
    kernel_type='laplace', approx_type='permutation', B1:int=500, B2:int=500, B3:int=100, weights_type='uniform', l_minus:int=0, l_plus:int=4, 
                                        alpha_:int=5, beta:int=10, penalty_type='L1', slice_size:int=10, overlap:int=1, max_iters:int=1500):
        """
        @param series - timeseries
        @param p_wnd_dim - past window size
        @param f_wnd_dim - future window size
        @param threshold - threshold for dynamic windowing
        @param alpha - real number in (0,1) (level of the test)
        @param kernel_type - "gaussian" or "laplace"
        @param approx_type - "permutation" (for MMD_a estimate Eq. (3)) or "wild bootstrap" (for MMD_b estimate Eq. (6))
        @param B1 - number of simulated test statistics to estimate the quantiles
        @param B2 - number of simulated test statistics to estimate the probability in Eq. (13) in our paper
        @param B3 - number of iterations for the bisection method output: result of MMDAgg (1 for "REJECT H_0" and 0 for "FAIL TO REJECT H_0")
        @param weights_type 
        @param l_minus - lower value in bandwidth search range
        @param l_plus - upper value in bandwidth search range
        @param alpha_ - default, 5
        @param beta - default, 10
        @param penalty_type - 'L1' or 'L2'
        @param slice_size - default, 10
        @param overlap - measure of granularity, default=1
        @param max_iters - maximum number of iterations, default=1500
        """
        super().__init__()
        self.p_wnd_dim = p_wnd_dim
        self.f_wnd_dim = f_wnd_dim
        self.series = series
        self.threshold = threshold
        self.alpha = alpha
        self.kernel_type = kernel_type
        self.approx_type = approx_type
        self.B1 = B1
        self.B2 = B2
        self.B3 = B3
        self.weights_type=weights_type
        self.l_minus=l_minus
        self.l_plus=l_plus
        self.alpha_ = alpha_
        self.beta = beta
        self.penalty_type = penalty_type
        self.slice_size = slice_size
        self.overlap = overlap
        self.max_iters = max_iters

        self.mmd_score, self.mmd_logit = self.dynamic_windowing(p_wnd_dim, f_wnd_dim, series, threshold, alpha, kernel_type, 
                                                    approx_type, B1, B2, B3, weights_type, l_minus, l_plus)

        self.corr_score = self.TVGL_(series=self.series, alpha = self.alpha_, beta =self.beta, penalty_type=self.penalty_type,
                                            slice_size=self.slice_size, overlap=self.overlap, threshold=self.threshold, max_iters=self.max_iters)

        #self.scores = self.mmd_score + abs(self.corr_score)

    def dynamic_windowing(self, p_wnd_dim, f_wnd_dim, series, threshold, alpha, kernel_type, approx_type, B1, B2, B3, weight_type, l_minus, l_plus):

        mmd_agg = np.asarray([])

        run_length = int(p_wnd_dim)
        i = p_wnd_dim

        while i <= len(series):
            prev = series[max(int(i)-run_length,0):int(i), :]
            next = series[max(int(i),0):int(i)+f_wnd_dim, :]

            if next.shape[0]<=2 or prev.shape[0]<=2:
                break

            hyp = mmdagg(123, prev, next, alpha=alpha, kernel_type=kernel_type, approx_type=approx_type,weights_type=weight_type, l_minus=l_minus, l_plus=l_plus, 
            B1 = B1, B2 = B2, B3 = B3)
            
            if hyp >=threshold:
                run_length = p_wnd_dim
                mmd_agg = np.concatenate((mmd_agg, np.repeat(hyp, 1)))
            else:   
                run_length += 1
                mmd_agg = np.concatenate((mmd_agg, np.repeat(0, 1)))
            i=i+1
        mmd_agg = np.absolute(mmd_agg)
        logit = (2./(1+np.exp(-3*(mmd_agg))))-1

        return mmd_agg, logit

    def visualize_results(self, series, scores, scores2, gt_cov, gt_mean, gt_var, label, label2):

        f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(series)
        ax1.plot(gt_cov, label = 'gt_cov')
        ax1.plot(gt_mean, label = 'gt_mean')
        ax1.plot(gt_var, label = 'gt_var')
        ax1.legend(loc="upper right")

        ax2.plot(scores, label = label)
        ax2.plot(scores2, label = label2)
        ax2.legend(loc="upper right")

        return plt

    def correlation_from_covariance(self, covariance):
        v = np.sqrt(np.diag(covariance))
        outer_v = np.outer(v, v)
        correlation = covariance / outer_v
        correlation[covariance == 0] = 0
        return correlation
    
    def TVGL_(self, series, alpha, beta, penalty_type, slice_size, overlap, threshold, max_iters):
        
        model = TVGL(alpha, beta, penalty_type, slice_size, overlap=overlap, max_iters=max_iters)

        model.fit(series)
        # set of precision matrice
        
        ps = model.precision_set
    
        corr_score = np.asarray([])

        ps_inv = [np.linalg.inv(ps[0])]
        for i in range(len(ps)):
            #x = ((ps[i])-(ps[i-1]))
            ps_inv_t = np.linalg.inv(ps[i])
            x = self.correlation_from_covariance(ps_inv_t)- self.correlation_from_covariance(ps_inv[-1])
            ps_inv.append(ps_inv_t)
            #x = (numpy.linalg.inv(ps[i]))- (numpy.linalg.inv(ps[i-1]))
            max_x = abs(x).max()
            #max_x = max(x.min(), x.max(), key=abs)
            #if abs(max_x) < 0:
            #    max_x = 0
            corr_score=np.concatenate((corr_score, np.repeat(max_x, 1)))
            corr_score=np.concatenate((corr_score, np.repeat(0, overlap-1)))

        if len(corr_score) > len(series):
            corr_score=corr_score[:len(series)]
        else:
            corr_score=np.concatenate((corr_score,np.zeros(int(series.shape[0]-len(corr_score)))))
        return corr_score


# KLCPD - Kernel Change Point Detection
class KLCPD():
    def __init__(self, series:np.array, p_wnd_dim:int=3, f_wnd_dim:int=3, epochs:int=10):
        """
        @param series - timeseries
        @param p_wnd_dim - past window size
        @param f_wnd_dim - future window size
        @param epochs - number of epochs
        """
        super().__init__()
        self.p_wnd_dim = p_wnd_dim
        self.f_wnd_dim = f_wnd_dim
        self.series = series
        self.epochs = epochs

        self.scores = self.klcpd(p_wnd_dim, f_wnd_dim, series, epochs)


    def klcpd(self, p_wnd_dim, f_wnd_dim, series, epochs):
        
        device = torch.device('cpu')

        model = KL_CPD(series.shape[1], p_wnd_dim=p_wnd_dim, f_wnd_dim = f_wnd_dim).to(device)

        model.fit(series, epoches=epochs)

        scores = model.predict(series)

        return scores

    def visualize_results(self, series, scores, gt_cov, gt_mean, gt_var, label):

        f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(series)
        ax1.plot(gt_cov, label = 'gt_cov')
        ax1.plot(gt_mean, label = 'gt_mean')
        ax1.plot(gt_var, label = 'gt_var')
        ax1.legend(loc="upper right")

        ax2.plot(scores, label = label)
        ax2.legend(loc="upper right")

        return plt

# graphtime 
class GRAPHTIME_CPD():
    def __init__(self, series:np.array, p_wnd_dim:int=10, f_wnd_dim:int=10, lambda1=0.1, lambda2=10, max_iter:int=1500):
        """
        @param series - timeseries
        @param p_wnd_dim - past window size
        @param f_wnd_dim - future window size
        @param lambda1 
        @param lambda2
        @param max_iters
        """
        super().__init__()
        self.p_wnd_dim = p_wnd_dim
        self.f_wnd_dim = f_wnd_dim
        self.series = series
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.max_iters = max_iter

        self.cps = self.graphtime_(p_wnd_dim, f_wnd_dim, series, max_iter, lambda1, lambda2)


    def graphtime_(self, p_wnd_dim, f_wnd_dim, series, max_iter, lambda1, lambda2):
        
        gfgl = GroupFusedGraphLasso(lambda1=lambda1, lambda2=lambda2, max_iter=max_iter)
        gfgl.fit(series)
        cps = get_change_points(gfgl.sparse_Theta, 1e-2)

        return cps

    def plot_data_with_cps(self, series, cps, ymin=None, ymax=None):
        ymin = np.min(series) if not ymin else ymin
        ymax = np.max(series) if not ymax else ymax
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(series, alpha=0.5)
        ax.set_ylabel('Values')
        ax.set_xlabel('Timestep')
        for cp in cps:
            ax.plot([cp, cp], [ymin, ymax], 'k-')
        ax.set_xlim([0, len(series)])
        ax.set_ylim([ymin, ymax])
        return fig

    def visualize_results(self, series, scores, gt_cov, gt_mean, gt_var, label):

        f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(series)
        ax1.plot(gt_cov, label = 'gt_cov')
        ax1.plot(gt_mean, label = 'gt_mean')
        ax1.plot(gt_var, label = 'gt_var')
        ax1.legend(loc="upper right")

        ax2.plot(scores, label = label)
        ax2.legend(loc="upper right")

        return plt

import scipy.stats
import numpy as np

def compute_conf_interval(cov_bases, mut_bases):
    assert len(cov_bases)==len(mut_bases), "cov_bases and mut_bases must be of same length"
    ci = {}
    i, ci['min'], ci['max'], ci['low'], ci['high'] = 0, np.zeros(len(cov_bases)), np.zeros(len(cov_bases)), np.zeros(len(cov_bases)), np.zeros(len(cov_bases))
    for cov, mut in zip(cov_bases, mut_bases):
        ci['min'][i], ci['max'][i] = tuple(np.array(scipy.stats.poisson.interval(0.95, mut))/cov)
        ci['low'][i], ci['high'][i] = mut/cov-ci['min'][i], ci['max'][i]-mut/cov
        i = i+1
    return ci

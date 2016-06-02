from scipy.optimize import leastsq
import numpy as np
import math
import random

def func_multi_linear(paras, ipt):
    if len(paras) != len(ipt):
        print "error: # paras <> # ipt"
        return -100
    opt = 0
    for i in range(len(paras)):
        opt += (paras[i] * ipt[i])
    return opt

def error_func(paras, ipts, opts):
    error_list = []
    for i in range(len(ipts)):
        error_list.append(func_multi_linear(paras, ipts[i]) - opts[i])
    return error_list

def series_cut(series, iptind, optind):
    if len(series)+1 < optind:
        print "series shorter than optind"
    series = np.array(series, dtype = "float")
    ipt = series[:iptind]
    opt = series[optind]
    return ipt, opt

def train(ipts, opts):
    paras_init = [0] * len(ipts[0])
    paras, success = leastsq(error_func, paras_init, args=(ipts, opts))
    print paras, success
    return paras

def test(ipts, opts, paras):
    n = len(ipts)
    Eseries = np.array(error_func(paras, ipts, opts))
    SSE = np.inner(Eseries, Eseries)
    RMSE = math.sqrt(SSE/n)
    RSE = 0
    for i in range(n):
        E = Eseries[i]
        if opts[i] > 0.0001:
            RE = E/opts[i]
        else:
            RE = E
        RSE += math.pow(RE, 2)
    RMRSE = math.sqrt(RSE/n)
    return RMSE, RMRSE

def validate(list_series_train, list_series_test, iptind, optind):
    ipts_train = []
    opts_train = []
    for series in list_series_train:
        ipt, opt = series_cut(series,iptind, optind)
        ipts_train.append(ipt)
        opts_train.append(opt)
    ipts_test = []
    opts_test = []
    for series in list_series_test:
        ipt, opt = series_cut(series,iptind, optind)
        ipts_test.append(ipt)
        opts_test.append(opt)
    paras = train(ipts_train,opts_train)
    print "paras:\n"
    print paras
    RMSE, RMRSE = test(ipts_test, opts_test, paras)
    print "input index until %d, output index at %d\n" % (iptind, optind)
    print "RMSE: %f" % RMSE
    print "RMRSE: %f" % RMRSE


def func_test_multiseries(paras, N):
    L = len(paras)
    list_series = []
    for i in range(N):
        series = np.random.random(L)
        list_series.append(np.append(series, np.inner(series, paras)+random.random()))
    return list_series

if __name__ =="__main__":
    ########### test ################
    paras0 = np.array([1,3,5,2,4,2,-4,-1,-2,-4,-5])
    ########### test ################

    list_series_train = func_test_multiseries(paras0, 1000)
    list_series_test = func_test_multiseries(paras0, 400)
    iptind = 11
    optind = 11
    validate(list_series_train, list_series_test, iptind, optind)
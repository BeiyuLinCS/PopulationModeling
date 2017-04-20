from __future__ import division
import numpy as np
import math
import itertools
from scipy.stats import t
from scipy.special import gammaln
def online_changepoint_detection(count, data0):

    l = data0.shape[0]
    maxes = np.zeros((count,1))
    R = np.zeros((count+1, 2))

    R[0, 0] = 1

    mu0    = 0
    kappa0 = 1
    alpha0 = 1
    beta0  = 1

    muT    = mu0
    kappaT = kappa0
    alphaT = alpha0
    betaT  = beta0

    muT0 = np.array([])
    kappaT0 = np.array([])
    alphaT0 = np.array([])
    betaT0 = np.array([])

    for k in range(0, count):
        data = data0[:, k]
        
        predprobs = t.pdf(data[0], df = 2*alphaT, loc = muT, scale = (betaT * (kappaT+1) / (alphaT * kappaT))**(0.5))
    
        H = [0.005]*(k+1)
        H2 = [0.995]*(k+1)
        
        R[1:k+2, 0+1] = R[0:k+1,0] * predprobs * H2
        R[0, 0+1] = np.sum(R[0:k+1,0] * predprobs * H)    
        R[:, 0+1] = R[:, 0+1] / np.sum(R[:, 0+1])

        muT0    =  np.append(mu0, (kappaT*muT + data[0])/ (kappaT+1.0))
        kappaT0 = np.append(kappa0, kappaT + 1.0)
        alphaT0 = np.append(alpha0, alphaT + 0.5)
        betaT0  = np.append(beta0, betaT + (kappaT*(data[0]-muT)**2)/(2.0*(kappaT+1)))
        
        muT     = muT0
        kappaT  = kappaT0
        alphaT  = alphaT0
        betaT   = betaT0
        
        maxes[k] = R[:,0].argmax()

        R = np.delete(R, np.s_[0], 1)
        R = np.c_[R, np.zeros(count+1)]
    return R, maxes
    
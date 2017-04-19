from __future__ import division
import numpy as np
from scipy.special import gammaln
import math
import itertools
def online_changepoint_detection(count, data0, observation_likelihood):

    #print("a.shape", data0.shape)  ## ('a.shape', (35, 713))
    # a = list(itertools.chain.from_iterable(a))
    # a = np.round(a, decimals=3)
    l = data0.shape[0]
    maxes = np.zeros((count+1,1))
    R = np.zeros((count+1, 2))

    R[0, 0] = 1

    for k in range(0, count):
        data = data0[:, k]
        t = 0 
        predprobs = observation_likelihood.pdf(data[t])
        H = [0.005]*(k+1)
        H2 = [0.995]*(k+1)
        predprobs = predprobs[:(k+1)]
    
        R[1:k+2, t+1] = R[0:k+1,t] * predprobs * H2
        R[0, t+1] = np.sum(R[0:k+1,t] * predprobs * H)    
        R[:, t+1] = R[:, t+1] / np.sum(R[:, t+1])

        mutest, kappatest, alphatest, betatest = observation_likelihood.update_theta(data[t])
        if k == count-1:
            maxes[k] = R[:,0].argmax()
            maxes[k+1] = R[:,1].argmax()    
        else:
            maxes[k] = R[:,0].argmax()

        R = np.delete(R, np.s_[0], 1)
        R = np.c_[R, np.zeros(count+1)]
    return R, maxes

class StudentT:
    def __init__(self, alpha, beta, kappa, mu):
        self.alpha0 = self.alpha = np.array([alpha])
        self.beta0 = self.beta = np.array([beta])
        self.kappa0 = self.kappa = np.array([kappa])
        self.mu0 = self.mu = np.array([mu])
        

    def pdf(self, data):
        nu = 2*self.alpha
        var = (self.beta * (self.kappa+1) / (self.alpha * self.kappa))
        mu = self.mu
        x = data
        c = [0]*len(nu)
        p = [0]*len(nu)
       
        for i in range(0, len(nu)):
            c[i] = math.exp(gammaln(nu[i]/2.0 + 0.5) - gammaln(nu[i]/2.0)) * (nu[i]*math.pi*var[i])**(-0.5);
            p[i] = c[i] * (1.0 + (1.0/(nu[i]*var[i]))*(x-mu[i])**2.0)**(-(nu[i]+1.0)/2.0);
        return p

    def update_theta(self, data):
        muT0 = np.concatenate((self.mu0, (self.kappa * self.mu + data) / (self.kappa + 1)))
        kappaT0 = np.concatenate((self.kappa0, self.kappa + 1.))
        alphaT0 = np.concatenate((self.alpha0, self.alpha + 0.5))
        betaT0 = np.concatenate((self.beta0, self.beta + (self.kappa * (data -
            self.mu)**2) / (2. * (self.kappa + 1.))))
            
        self.mu = muT0
        self.kappa = kappaT0
        self.alpha = alphaT0
        self.beta = betaT0
        return (self.mu, self.kappa, self.alpha, self.beta)




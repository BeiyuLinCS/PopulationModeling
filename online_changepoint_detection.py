from __future__ import division
import numpy as np
from scipy.special import gammaln
import math
from scipy.sparse import lil_matrix
import scipy.sparse
import itertools
from scipy.sparse import csr_matrix


def online_changepoint_detection(count, data, observation_likelihood):
    maxes = np.zeros((count,1))
    R = lil_matrix((count+2, count+1))   ## sparse matrix
    R[1:,1:] = 0
    R[0, 0] = 1

    for t in range(0, count):
        
        mutest = 0
        kappatest = 0
        alphatest = 0
        betatest = 0

        predprobs = lil_matrix(observation_likelihood.pdf(data[t]))
    
        h_temp = hazard_func(np.array(range(0,t+1)))
        H = lil_matrix(h_temp)   # H will be always the same.
        
        ones = lil_matrix([1]*(H.shape[1]))

        R[1:t+2, t+1] = (R[0:t+1,t].toarray() * predprobs.T.toarray())*((ones-H).T.toarray())
        
        R[0, t+1] = np.sum(R[0:t+1,t].toarray() * predprobs.T.toarray() * (H.T.toarray()))
        
        temp_a = (1.0/np.sum(R[:, t+1].toarray()))
        temp_b = lil_matrix([temp_a])
        
        R[:, t+1] = R[:, t+1] * (temp_b)
        
        mutest, kappatest, alphatest, betatest = observation_likelihood.update_theta(data[t])

        temp_R = csr_matrix(R[:,t])
        
        maxes[t] = temp_R.data.argmax()
    
    return R, maxes


def hazard_func(r):
    lam = 200
    return 1/lam * np.ones(r.shape)


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
        #return list(itertools.chain.from_iterable(p))
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




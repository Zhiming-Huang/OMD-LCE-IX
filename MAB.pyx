#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 20:45:35 2022

@author: zhiming
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

class MAB:
    def __init__(self,K,opt):
        # initialize the action set
       # self.actions = actions
        self.K = K
        # initialize the probabiltiy distribution
        # self.eta = np.log(K)/t
        self.t = 1
        self.meta_dis = np.ones([self.K, self.K]) / self.K
        self.L = np.zeros([self.K, self.K])
        self.p = np.ones(self.K)/self.K
        self.beta = (np.log(K)/self.t)
        self.opt = opt # 0 for LCE, 1 for LCE-IX, 2 for OMD-LCE-IX

    def __Markov_Steady_State_Prop(self):
        Q = np.mat(self.meta_dis)
        E = np.eye(self.K)
        p = np.vstack([Q.T - E, np.ones(self.K)]).I * np.vstack([np.zeros([self.K, 1]), 1])
        self.p = np.array(p.T)[0]
        

    def draw_action(self):
        return np.random.choice(range(self.K), p=self.p)

    def update_dist(self, action, r):
        if self.opt == 0:
            return self.__LCE(action,r)
        elif self.opt == 1:
            return self.__LCE_IX(action,r)
        elif self.opt == 2:
            return self.__OMD(action,r)

    def __LCE_IX(self, action, r):
        eta = (np.log(self.K) / self.t) ** 0.5
        gamma = (np.log(self.K) / (self.t+1)) ** 0.5 / 2
        q = np.reshape(self.meta_dis[:, action], self.K)
        self.L[:, action] += (1 - r) * (self.p * q   / self.p[action] ) / (gamma + q)
        for i in range(self.K):
            self.meta_dis[i, :] = np.exp(-eta * self.L[i, :]) / np.sum(
                np.exp(-eta * self.L[i, :])
            )
        self.__Markov_Steady_State_Prop()
        self.t += 1

    
    def __LCE(self,action,r):
        eta = (np.log(self.K) / self.t) ** 0.5
        self.L[:, action] += (1 - r) * (self.p / self.p[action])
        for i in range(self.K):
            self.meta_dis[i, :] = np.exp(-eta * self.L[i, :]) / np.sum(
                np.exp(-eta * self.L[i, :])
            )
        self.__Markov_Steady_State_Prop()
        self.t += 1

    def __OMD(self, action, r):
        eta = (np.log(self.K) / self.t) ** 0.5
        gamma = (np.log(self.K) / ((self.t+1))) ** 0.5 / 2
        tempq = self.meta_dis ** -0.5
        q = np.reshape(self.meta_dis[:, action], self.K)
        tempq[:, action] += eta * (1 - r) * (self.p * q   / self.p[action] ) / (gamma + q)
        for i in range(self.K):
            lambdax = -1
            while True:
                sumq = np.sum((tempq[i,:] + lambdax)**(-2)) - 1
                if np.abs(sumq) < 0.0001:
                    break
                dsumq = np.sum(-2 * (tempq[i,:] + lambdax)**(-3))
                lambdax = lambdax - sumq/dsumq
            self.meta_dis[i, :] = (tempq[i,:] + lambdax)**(-2)
        self.__Markov_Steady_State_Prop()
        self.t += 1


if __name__ == "__main__":
    # module test program
    instance = MAB(2,0)
    instance2 = MAB(2,1)
    instance3 = MAB(2,2)
    T = 1000
    
    #generate a multivariable gaussian distribution  
    lowarm = np.random.uniform(0,0.4,[1, T])
    higharm = np.random.uniform(0.8,1,[1, T])

    rewards = np.vstack([higharm, lowarm])
    
    reward = np.zeros(T)
    time_ave_reward = np.zeros(T)
    
    reward2 = np.zeros(T)
    time_ave_reward2 = np.zeros(T)

    reward3 = np.zeros(T)
    time_ave_reward3 = np.zeros(T)

    reward4 = np.zeros(T)
    time_ave_reward4 = np.zeros(T)
    for t in range(T):
        # LCE selection
        action = instance.draw_action()
        r = rewards[action,t]
        instance.update_dist(action, r)
        reward[t] = r
        # LCE-IX selection
        action = instance2.draw_action()
        r = rewards[action,t]
        instance2.update_dist(action, r)
        reward3[t] = r
        # OMD-LCE-IX selection
        action = instance3.draw_action()
        r = rewards[action,t]
        instance3.update_dist(action, r)
        reward4[t] = r
        # random selection
        action = np.random.choice(range(2), p=[0.5,0.5])
        reward2[t] = rewards[action,t]
        
        
    cumureward = np.cumsum(reward)
    cumureward2 = np.cumsum(reward2)
    cumureward3 = np.cumsum(reward3)
    cumureward4 = np.cumsum(reward4)
    opt = max(np.sum(rewards,axis = 1)/T)
    for t in range(T):
        time_ave_reward[t] = cumureward[t]/(t+1)
        time_ave_reward2[t] = cumureward2[t]/(t+1)
        time_ave_reward3[t] = cumureward3[t]/(t+1)
        time_ave_reward4[t] = cumureward4[t]/(t+1)
    l1 = plt.plot(time_ave_reward, label = 'LCE')
    l2 = plt.plot(time_ave_reward2, label = 'Random')
    l3 = plt.plot(time_ave_reward3, label = 'LCE-IX')
    l4 = plt.plot(time_ave_reward4, label = 'OMD-LCE-IX')
    plt.legend()

# %%

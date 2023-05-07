#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： Chen Dan
# Time ： 2023/5/4 13:04
from utils import *


if __name__ == '__main__':
    filename = ["01_Jazz", "02_USAir",
                "03_Netscience", "04_EEC", "05_Email", 
                "06_Euroroad","07_Blogs", "08_Facebook", "09_GrQc",
                "10_Power", "11_Router", "12_PG", "13_WikiVote",
                "14_Sex", "15_Enron", "16_coauthor_1992"]


    nums = 11
    gamma = 1.0  # recovery rate
    tmin, tmax = 0.0, 50.0
    iterations = 1000
    report_times = np.linspace(tmin, tmax, 21)


    for name in filename:
        print(name)
        G = load_graph_data(name)
        N, M = len(G.nodes()), len(G.edges())
        print(N, M)


        # epidemic threshold: beta_c
        beta_c = get_beta_c(G, N)
        print("beta_c: ", beta_c)
        beta_list = np.linspace(0.5, 1.5, nums) * beta_c  # infection probability $\beta$

        SR = np.zeros((N, nums+1)) # standard ranking
        for j, beta in enumerate(beta_list):
            for i in G.nodes():
                obs_R = 0 * report_times
                for counter in range(iterations):
                    t, S, I, R = EoN.fast_SIR(G, beta, gamma, initial_infecteds=i, tmax=tmax)
                    obs_R += EoN.subsample(report_times, t, R)

                SR[i, j+1] = obs_R[-1] / iterations
        SR[:,0] = np.array(list(G.nodes())) # The first column holds the node labels. Note that node labels range from 0 to N-1.
        np.savetxt("./standard_ranking_results/standard_ranking_" + name + ".csv", SR, delimiter=',', fmt='%f')
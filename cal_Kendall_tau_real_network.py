#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： Chen Dan
# Time ： 2023/5/5 11:11
from utils import *
from ehcc import *


if __name__ == '__main__':
    filename = ["01_Jazz", "02_USAir",
                "03_Netscience", "04_EEC", "05_Email", 
                "06_Euroroad","07_Blogs", "08_Facebook", "09_GrQc",
                "10_Power", "11_Router", "12_PG", "13_WikiVote",
                "14_Sex", "15_Enron", "16_coauthor_1992", "BA_0"]

    R = 2
    nums = 11
    for name in filename[:1]:
        print(name)
        G = load_graph_data(name)
        N, M = len(G.nodes()), len(G.edges())
        print(N, M)

        beta_c = get_beta_c(G, N)

        DC = dict(nx.degree(G))
        KS = nx.core_number(G)
        CC = nx.closeness_centrality(G)
        EC = nx.eigenvector_centrality(G, max_iter=10000)
        SP = cal_SP(G)
        EHCC = EHCC_main(G, 0.5)
        DC_AND = DC_plus(G)

        nodes = list(G.nodes())

        if name != '16_coauthor_1992':
            DM = get_distance_matrix(G, N)
            DCGM, GGC, DCGM1, DCGM2 = GM_model(R, nodes, DM, DC, SP, DC_AND)
        else:
            DCGM, GGC, DCGM1, DCGM2 = GM_model2(G, R, nodes, DC, SP, DC_AND)

        
        X1 = list(DC.values())
        X2 = list(KS.values())
        X3 = list(CC.values())
        X4 = list(EC.values())
        X5 = list(DCGM.values())
        X6 = list(GGC.values())
        X7 = list(EHCC.values())
        X8 = list(DC_AND.values())
        X9 = list(DCGM1.values())
        X10 = list(DCGM2.values())


        beta_list = np.linspace(0.5, 1.5, nums) * beta_c
        tau_list1 = np.zeros(nums)
        tau_list2 = np.zeros(nums)
        tau_list3 = np.zeros(nums)
        tau_list4 = np.zeros(nums)
        tau_list5 = np.zeros(nums)
        tau_list6 = np.zeros(nums)
        tau_list7 = np.zeros(nums)
        tau_list8 = np.zeros(nums)
        tau_list9 = np.zeros(nums)
        tau_list10 = np.zeros(nums)


        # standard ranking
        SR = np.loadtxt("./standard_ranking_results/standard_ranking_" + name + ".csv", delimiter=',', dtype=np.float64)
        outf = open("./Kendall_tau_results/Kendall_tau_" + name + ".dat", "w")
        for i, beta in enumerate(beta_list):
            SRi = SR[:, i+1]
            Y = list(SRi)
            tau_list1[i] = cal_Kendall_tau_coefficient(X1, Y)
            tau_list2[i] = cal_Kendall_tau_coefficient(X2, Y)
            tau_list3[i] = cal_Kendall_tau_coefficient(X3, Y)
            tau_list4[i] = cal_Kendall_tau_coefficient(X4, Y)
            tau_list5[i] = cal_Kendall_tau_coefficient(X5, Y)
            tau_list6[i] = cal_Kendall_tau_coefficient(X6, Y)
            tau_list7[i] = cal_Kendall_tau_coefficient(X7, Y)
            tau_list8[i] = cal_Kendall_tau_coefficient(X8, Y)
            tau_list9[i] = cal_Kendall_tau_coefficient(X9, Y)
            tau_list10[i] = cal_Kendall_tau_coefficient(X10, Y)

            outf.write(str(beta/beta_c) + " " + str(tau_list1[i]) + " " + str(tau_list2[i]) +
                       " " + str(tau_list3[i]) + " " + str(tau_list4[i]) +
                       " " + str(tau_list5[i]) + " " + str(tau_list6[i]) +
                       " " + str(tau_list7[i]) + " " + str(tau_list8[i]) +
                       " " + str(tau_list9[i]) + " " + str(tau_list10[i]) + "\n")

        outf.close()
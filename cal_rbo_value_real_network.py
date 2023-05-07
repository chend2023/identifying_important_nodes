#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： Chen Dan
# Time ： 2023/5/6 21:48
from utils import *
from ehcc import *
import rbo


if __name__ == '__main__':
    filename = ["01_Jazz", "02_USAir",
                "03_Netscience", "04_EEC", "05_Email", 
                "06_Euroroad","07_Blogs", "08_Facebook", "09_GrQc",
                "10_Power", "11_Router", "12_PG", "13_WikiVote",
                "14_Sex", "15_Enron", "16_coauthor_1992"]

    R = 2
    nums = 11
    for name in filename[:1]:
        print(name)
        G = load_graph_data(name)
        N, M = len(G.nodes()), len(G.edges())
        print(N, M)

        beta_c = get_beta_c(G, N)
        print("beta_c: ", beta_c)

        DC = dict(nx.degree(G))
        sorted_DC = dict(sorted(DC.items(), key=lambda x: x[1], reverse=True))
        KS = nx.core_number(G)
        sorted_KS = dict(sorted(KS.items(), key=lambda x: x[1], reverse=True))
        CC = nx.closeness_centrality(G)
        sorted_CC = dict(sorted(CC.items(), key=lambda x: x[1], reverse=True))
        EC = nx.eigenvector_centrality(G, max_iter=10000)
        sorted_EC = dict(sorted(EC.items(), key=lambda x: x[1], reverse=True))
        SP = cal_SP(G)
        EHCC = EHCC_main(G, 0.5)
        sorted_EHCC = dict(sorted(EHCC.items(), key=lambda x: x[1], reverse=True))
        DC_AND = DC_plus(G)
        sorted_DC_AND = dict(sorted(DC_AND.items(), key=lambda x: x[1], reverse=True))

        nodes = list(G.nodes())

        if name != '16_coauthor_1992':
            DM = get_distance_matrix(G, N)
            DCGM, GGC, DCGM1, DCGM2 = GM_model(R, nodes, DM, DC, SP, DC_AND)
        else:
            print("==========")
            DCGM, GGC, DCGM1, DCGM2 = GM_model2(G, R, nodes, DC, SP, DC_AND)
        sorted_DCGM = dict(sorted(DCGM.items(), key=lambda x: x[1], reverse=True))
        sorted_GGC = dict(sorted(GGC.items(), key=lambda x: x[1], reverse=True))
        sorted_DCGM1 = dict(sorted(DCGM1.items(), key=lambda x: x[1], reverse=True))
        sorted_DCGM2 = dict(sorted(DCGM2.items(), key=lambda x: x[1], reverse=True))



        X1 = list(sorted_DC.keys())
        X2 = list(sorted_KS.keys())
        X3 = list(sorted_CC.keys())
        X4 = list(sorted_EC.keys())
        X5 = list(sorted_DCGM.keys())
        X6 = list(sorted_GGC.keys())
        X7 = list(sorted_EHCC.keys())
        X8 = list(sorted_DC_AND.keys())
        X9 = list(sorted_DCGM1.keys())
        X10 = list(sorted_DCGM2.keys())


        beta_list = np.linspace(0.5, 1.5, nums) * beta_c
        rbo_list1 = np.zeros(nums)
        rbo_list2 = np.zeros(nums)
        rbo_list3 = np.zeros(nums)
        rbo_list4 = np.zeros(nums)
        rbo_list5 = np.zeros(nums)
        rbo_list6 = np.zeros(nums)
        rbo_list7 = np.zeros(nums)
        rbo_list8 = np.zeros(nums)
        rbo_list9 = np.zeros(nums)
        rbo_list10 = np.zeros(nums)


        # standard ranking
        SR = np.loadtxt("./standard_ranking_results/standard_ranking_" + name + ".csv", delimiter=',', dtype=np.float64)
        outf = open("./rbo_value/rbo_value_" + name + ".dat", "w")
        for i, beta in enumerate(beta_list):
            SRi = dict(zip(SR[:, 0], SR[:, i+1]))
            sorted_SRi = dict(sorted(SRi.items(), key=lambda x: x[1], reverse=True))
            Y = list(sorted_SRi.keys())

            rbo_list1[i] = rbo.RankingSimilarity(X1, Y).rbo()
            rbo_list2[i] = rbo.RankingSimilarity(X2, Y).rbo()
            rbo_list3[i] = rbo.RankingSimilarity(X3, Y).rbo()
            rbo_list4[i] = rbo.RankingSimilarity(X4, Y).rbo()
            rbo_list5[i] = rbo.RankingSimilarity(X5, Y).rbo()
            rbo_list6[i] = rbo.RankingSimilarity(X6, Y).rbo()
            rbo_list7[i] = rbo.RankingSimilarity(X7, Y).rbo()
            rbo_list8[i] = rbo.RankingSimilarity(X8, Y).rbo()
            rbo_list9[i] = rbo.RankingSimilarity(X9, Y).rbo()
            rbo_list10[i] = rbo.RankingSimilarity(X10, Y).rbo()


            outf.write(str(beta/beta_c) + " " + str(rbo_list1[i]) + " " + str(rbo_list2[i]) +
                       " " + str(rbo_list3[i]) + " " + str(rbo_list4[i]) +
                       " " + str(rbo_list5[i]) + " " + str(rbo_list6[i]) +
                       " " + str(rbo_list7[i]) + " " + str(rbo_list8[i]) +
                       " " + str(rbo_list9[i]) + " " + str(rbo_list10[i]) + "\n")

        outf.close()

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： Chen Dan
# Time ： 2023/5/5 14:25
from utils import *
from ehcc import *


if __name__ == '__main__':
    R = 2
    nums = 11
    samples = 20
    name = "ER"
    # name = "BA"
    tau_list0 = np.zeros((10, nums))

    gamma = 1.0  # recovery rate
    tmin, tmax = 0.0, 50.0
    iterations = 1000
    report_times = np.linspace(tmin, tmax, 21)
    N = 500
    M = 3*N
    m = 3
    for c in range(samples):
        print("==========")
        G = nx.gnm_random_graph(N, M)
        # G = nx.barabasi_albert_graph(N, m)
        beta_c = get_beta_c(G, N)
        beta_list = np.linspace(0.5, 1.5, nums) * beta_c

        DC = dict(nx.degree(G))
        KS = nx.core_number(G)
        CC = nx.closeness_centrality(G)
        EC = nx.eigenvector_centrality(G, max_iter=10000)
        SP = cal_SP(G)
        EHCC = EHCC_main(G, 0.5)
        DC_AND = DC_plus(G)

        nodes = list(G.nodes())

        DM = get_distance_matrix(G, N)
        DCGM, GGC, DCGM1, DCGM2 = GM_model(R, nodes, DM, DC, SP, DC_AND)

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

        tau_list = np.zeros((10, nums))
        for i, beta in enumerate(beta_list):
            SR = get_SIR_ranking(G, beta, gamma, tmax, report_times, iterations)
            Y = list(SR.values())
            tau_list[0, i] = cal_Kendall_tau_coefficient(X1, Y)
            tau_list[1, i] = cal_Kendall_tau_coefficient(X2, Y)
            tau_list[2, i] = cal_Kendall_tau_coefficient(X3, Y)
            tau_list[3, i] = cal_Kendall_tau_coefficient(X4, Y)
            tau_list[4, i] = cal_Kendall_tau_coefficient(X5, Y)
            tau_list[5, i] = cal_Kendall_tau_coefficient(X6, Y)
            tau_list[6, i] = cal_Kendall_tau_coefficient(X7, Y)
            tau_list[7, i] = cal_Kendall_tau_coefficient(X8, Y)
            tau_list[8, i] = cal_Kendall_tau_coefficient(X9, Y)
            tau_list[9, i] = cal_Kendall_tau_coefficient(X10, Y)

        tau_list0 += tau_list


    beta_list0 = np.linspace(0.5, 1.5, nums)
    outf = open("./Kendall_tau_results/Kendall_tau_" + name + ".dat", "w")
    tau_list0 = (tau_list0/samples).transpose()
    for i in range(len(beta_list0)):
        outf.write(str(beta_list0[i]) + " " + str(tau_list0[i, 0]) + " " + str(tau_list0[i, 1]) +
                    " " + str(tau_list0[i, 2]) + " " + str(tau_list0[i, 3]) +
                    " " + str(tau_list0[i, 4]) + " " + str(tau_list0[i, 5]) +
                    " " + str(tau_list0[i, 6]) + " " + str(tau_list0[i, 7]) +
                    " " + str(tau_list0[i, 8]) + " " + str(tau_list0[i, 9]) + "\n")

    outf.close()
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author ： Chen Dan
# Time ： 2023/5/5 13:43
import networkx as nx
import EoN
import numpy as np
from scipy import stats
import igraph as ig
from collections import Counter


# Load real network data to generate the network
def load_graph_data(name):
    G = nx.read_edgelist("./network_edgelist/" + name + ".edgelist", nodetype=np.int64)
    N = nx.number_of_nodes(G)
    mapping = dict(zip(G, range(N)))
    G = nx.relabel_nodes(G, mapping)
    return G


# epidemic threshold: beta_c
def get_beta_c(G, N):
    k = sum([G.degree(i) for i in G.nodes()])/N
    square_k = sum([G.degree(i)**2 for i in G.nodes()])/N

    return k/(square_k-k)

# DC^{+}
def DC_plus(G):
    av_nei_deg = nx.average_neighbor_degree(G)
    DC_AND = {i : G.degree(i)*av_nei_deg[i] for i in G.nodes()}

    return DC_AND


# Calculate the shortest path distance matrix of the network
def get_distance_matrix(G, N):
    g = ig.Graph.from_networkx(G)
    DM = np.array(g.shortest_paths()).reshape(N,N)

    return DM


# references: Li H, Shang Q, Deng Y. A generalized gravity model for influential spreaders identification in complex networks[J].
# Chaos, Solitons & Fractals, 2021, 143: 110456.
def cal_SP(G):
    SP = {}
    for i in G.nodes():
        ci = nx.clustering(G, i)
        SP[i] = np.exp(-2.0*ci)*G.degree(i)
    return SP


# gravity model
def GM_model(R, nodes, DM, DC, SP, DC_AND):
    DCGM = {}
    GGC = {}
    DCGM1 = {}
    DCGM2 = {}

    for i in nodes:
        s1 = 0
        s2 = 0
        s3 = 0
        index_j = np.argwhere(DM[i]<=R).flatten()
        for j in index_j:
            dij = DM[i,j]
            if dij>0:
                s1 += (DC[i] * DC[j]) / (dij ** 2)
                s2 += (SP[i] * SP[j]) / (dij ** 2)
                s3 += (DC_AND[i] * DC_AND[j]) / (dij ** 2)
        DCGM[i] = s1
        GGC[i] = s2
        DCGM1[i] = s3
        DCGM2[i] = DC_AND[i]*s1

    return DCGM, GGC, DCGM1, DCGM2


def GM_model2(G, R, nodes, DC, SP, DC_AND):
    g = ig.Graph.from_networkx(G)
    DCGM = {}
    GGC = {}
    DCGM1 = {}
    DCGM2 = {}

    for i in nodes:
        s1 = 0
        s2 = 0
        s3 = 0
        ball_i_R = set(g.neighborhood(i, order=R))
        ball_i_R.remove(i)
        for j in ball_i_R:
            dij = g.distances(i, j)[0][0]
            if dij>0:
                s1 += (DC[i] * DC[j]) / (dij ** 2)
                s2 += (SP[i] * SP[j]) / (dij ** 2)
                s3 += (DC_AND[i] * DC_AND[j]) / (dij ** 2)
        DCGM[i] = s1
        GGC[i] = s2
        DCGM1[i] = s3
        DCGM2[i] = DC_AND[i]*s1

    return DCGM, GGC, DCGM1, DCGM2


def get_SIR_ranking(G, beta, gamma, tmax, report_times, iterations):
    SR = {}
    for i in G.nodes():
        obs_R = 0 * report_times
        for counter in range(iterations):
            t, S, I, R = EoN.fast_SIR(G, beta, gamma, initial_infecteds=i, tmax=tmax)
            obs_R += EoN.subsample(report_times, t, R)

        SR[i] = obs_R[-1] / iterations

    return SR


def cal_Kendall_tau_coefficient(X, Y):
    tau, p_value = stats.kendalltau(X, Y)
    return tau


def cal_spearman_r_coefficient(X, Y):
    a = stats.spearmanr(X, Y)
    return a[0]

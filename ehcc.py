import networkx as nx  # the networkx package
import copy

# references: Liu J, Zheng J. Identifying important nodes in complex networks based on extended degree and E-shell hierarchy decomposition[J].
# Scientific Reports, 2023, 13(1): 3197.

def arg_min(x):  # argmin function for dict type
    '''
    x: a dict
    '''
    y = min([x[key] for key in x.keys()])  # the minimum value
    z = []  # contains keys with the minimum value
    for key in x.keys():
        if x[key] == y:
            z.append(key)
    return z


def ex_deg(g, delta):  # extended degree
    dict_exdeg = {}  # contains node extended degree
    for node in g.nodes():
        exdeg = delta * g.degree[node]
        for neighbor in g.neighbors(node):
            exdeg += (1 - delta) * g.degree[neighbor]
        dict_exdeg[node] = exdeg  # calculate node extended degree
    return dict_exdeg


def E_shell_decomp(g, delta):  # E-shell hierarchy decomposition
    pos = {}  # contain position index of nodes
    pos_index = 0  # position index
    while g:
        pos_index += 1
        dict_exdeg = ex_deg(g,delta)  # calculate extended degree for current network
        min_nodes = arg_min(dict_exdeg)  # find the nodes with minimum extended degree
        for i in min_nodes:
            pos[i] = pos_index  # assign position index to min nodes
        g.remove_nodes_from(min_nodes)  # delete min nodes from current network
    return pos


def EHCC_main(g, delta):  # main program of EHCC
    '''
    g: input a network
    delta: a weight parameter in [0,1]
    '''
    g_1 = copy.deepcopy(g)  # copy the network
    extended_degree = ex_deg(g,delta)  # calculate extended degree
    pos = E_shell_decomp(g_1,delta)  # calculate position index
    max_exdeg = max([extended_degree[node] for node in g.nodes()])  # maximal extended degree
    max_pos = max([pos[node] for node in g.nodes()]) # maximal position index
    hcc = {}  # contain hcc value of nodes
    for node in g.nodes():
        hcc[node] = extended_degree[node] / max_exdeg + pos[node] / max_pos
    ehcc = {}  # contain ehcc value of nodes
    for node in g.nodes():
        temp = hcc[node]
        for neighbor in g.neighbors(node):
            temp += hcc[neighbor]
        ehcc[node] = temp
    return ehcc

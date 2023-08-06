#
#    Copyright (C) 2018 by
#    Thomas Bonald <thomas.bonald@telecom-paristech.fr>
#    Bertrand Charpentier <bertrand.charpentier@live.fr>
#    All rights reserved.
#    BSD license.

#    almost all of the code comes from:
#    https://github.com/tbonald/paris/blob/master/utils.py

import io
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from scipy.cluster.hierarchy import dendrogram, to_tree

from krakow import krakow

# from louvain import louvain


def generate_shuffled_graph(G):
    """
    You can use it on a graph before passing it to a clustering algorithm.
    This way you may get slightly different clustering at the end.
    """
    edges = list(G.edges(data=True))
    np.random.shuffle(edges)
    New_graph = nx.from_edgelist(edges)
    return New_graph


def split_into_n_children(tree, n):
    """Cut the biggest cluster in two, and repeat until there are n clusters.

    Can throw ValueError if the tree cannot be further divided.
    """
    children = [tree]

    while len(children) < n:
        index_of_biggest = np.argmax([child.count for child in children])
        to_split = children[index_of_biggest]
        if to_split.is_leaf():
            raise ValueError("tree cannot be further divided")
        splitten = [to_split.left, to_split.right]
        children[index_of_biggest : index_of_biggest + 1] = splitten
        # print([child.count for child in children])
    return children


def create_dendrogram(D, clusters_limit=None, width=10, height=4):
    """
    If clusters limit is None, then all clusters are shown, without any limit.
    """
    # a hack to disable plotting, only return the image
    was_interactive = plt.isinteractive()
    plt.ioff()

    _ = plt.figure(figsize=(width, height))
    # display logarithm of cluster distances
    Dlog = D.copy()
    Dlog[:, 2] = np.log(Dlog[:, 2])
    if clusters_limit is not None:
        # cut off the bottom part of the plot as it's not informative
        Dlog[:, 2][:-clusters_limit] *= 0
        Dlog[-clusters_limit:, 2] = Dlog[-clusters_limit:, 2] - Dlog[-clusters_limit, 2]
        dendrogram(Dlog, leaf_rotation=90.0, truncate_mode="lastp", p=clusters_limit)
    else:
        Dlog[:, 2] = Dlog[:, 2] - Dlog[0, 2]
        dendrogram(Dlog, leaf_rotation=90.0)

    plt.axis("off")
    img = io.BytesIO()
    plt.savefig(img, bbox_inches="tight")

    # revert to the previous plt state
    if was_interactive:
        plt.ion()
    return img


def _depth_of_leaves(tree):
    if tree.is_leaf():
        return [0]

    left = _depth_of_leaves(tree.left)
    right = _depth_of_leaves(tree.right)

    return [depth + 1 for depth in left + right]


def get_disbalance(tree):
    """
    how much higher is the average leaf depth, than in an ideally balanced tree
    """
    depths = _depth_of_leaves(tree)
    return np.average(depths) - np.log2(tree.count)


def _balance_on_single_node(node):
    """
    ideal balance (0.5, 0.5) gives a score 0
    any inbalance returns negative score
    """
    if node.is_leaf() or node.left.is_leaf() or node.right.is_leaf():
        # TODO is this robust? maybe give some penalty instead
        # this will never be a problem if we stay near the top layers
        return 0
    left_ratio = node.left.count / node.count
    right_ratio = node.right.count / node.count
    return 2 + np.log2(left_ratio) + np.log2(right_ratio)


def get_top_levels_balance_log(tree, levels=5):
    """
    how disbalanced are top levels of the tree
    any inbalance returns negative score, 0 is perfect
    """
    balance_on_levels = []

    nodes = [tree]
    for _ in range(levels):
        balances_on_one_level = [_balance_on_single_node(node) for node in nodes]
        balance_on_levels.append(np.average(balances_on_one_level))

        new_nodes = []
        for node in nodes:
            if node.is_leaf():
                continue
            if node.left is not None:
                new_nodes.append(node.left)
            if node.right is not None:
                new_nodes.append(node.right)
        nodes = new_nodes

    return np.average(balance_on_levels)


def help_finding_optimal_alpha(G, alphas, clusters_limit=None, width=10, height=4, levels=5):
    """
    Runs the clustering for each specified alpha value, for graph G.
    For each clustering prints it's quality and disbalance.
    """
    for alpha in alphas:
        dendrogram = krakow(G, alpha=alpha, beta=1)
        tree = to_tree(dendrogram)

        print(f"\nalpha = {alpha}")
        print(f"Disbalance: {get_disbalance(tree):.3f}")
        print(f"Top levels balance: {get_top_levels_balance_log(tree, levels=levels):.3f}")
        print(f"Clustering quality: {1 - normalized_dasgupta_cost(G, dendrogram):.3f}")
        img = create_dendrogram(
            dendrogram, clusters_limit=clusters_limit, width=width, height=height
        )
        try:
            display(Image.open(img))
        except NameError:
            print("Cannot display dendrogram, please run this in IPython")
            pass


#########################
### Display functions ###
#########################

# Plot k best clusterings
def plot_best_clusterings(G, D, k, pos, width=16, height=8):
    nb_plot = 2
    k1 = min(k, nb_plot)
    k2 = max(1, k // nb_plot)
    colors = [
        "b",
        "g",
        "r",
        "c",
        "m",
        "y",
        "k",
        "0.5",
        "0.3",
        "0.8",
        "0.6",
        "0.2",
        "0.7",
        "0.1",
        "0.9",
    ]
    plt.rcParams.update({"font.size": 24})
    plt.figure(figsize=(k1 * width, k2 * height))
    plt.subplots_adjust(left=0.02, right=0.98, bottom=0.06, top=0.85, wspace=0.05, hspace=0.05)
    for i in range(k):
        clustering = best_clustering(D, i)
        length = [len(c) for c in clustering]
        index = np.argsort(-np.array(length))

        plt.subplot(k2, k1, i + 1)
        plt.axis("off")
        plt.title("Rank: " + str(i + 1) + "\n(#clusters=" + str(len(clustering)) + ")")
        draw_nodes = nx.draw_networkx_nodes(G, pos, node_size=50, node_color="w")
        draw_nodes.set_edgecolor("k")
        nx.draw_networkx_edges(G, pos, alpha=0.1)
        nodes = list(G.nodes())
        for l in range(min(len(clustering), len(colors))):
            nodelist = [nodes[i] for i in clustering[index[l]]]
            draw_nodes = nx.draw_networkx_nodes(
                G, pos, node_size=50, nodelist=nodelist, node_color=colors[l]
            )
            draw_nodes.set_edgecolor("k")
    plt.show()


# Print names of the elements of the k largest clusters
def show_largest_clusters(C, G, name, k=10):
    index = np.argsort([-len(c) for c in C])
    for l in range(k):
        c = C[index[l]]
        index_node = np.argsort([-G.degree(u) for u in c])
        print("#" + str(l + 1))
        print("Size = " + str(len(c)))
        cluster_list = ""
        for i in range(min(10, len(c))):
            u = c[index_node[i]]
            cluster_list += name[u] + ", "
        print(cluster_list[:-2] + "\n")


###################################################
### Cluster and clustering extraction functions ###
###################################################

# Rank clusterings at every level of the dendrogram
def rank_clustering(D):
    logdist = np.log(D[:, 2])
    delta = logdist[1:] - logdist[:-1]
    return np.argsort(-delta[len(delta) // 2 :]) + 1 + len(delta) // 2


# Select the k-th best clustering
def best_clustering(D, k=0):
    return select_clustering(D, rank_clustering(D)[k])


# Select the clustering after k merges
def select_clustering(D, k):
    n = np.shape(D)[0] + 1
    k = min(k, n - 1)
    cluster = {i: [i] for i in range(n)}
    for t in range(k):
        cluster[n + t] = cluster.pop(int(D[t][0])) + cluster.pop(int(D[t][1]))
    return sorted(cluster.values(), key=len, reverse=True)


# Extract the clusters low level clusters contained in a high level cluster
def extract_subclusters(c_high_level, clustering_low_level):
    subclusters = []
    for c in clustering_low_level:
        if len(list(set(c_high_level) & set(c))) > 0:
            subclusters.append(c)
    return subclusters


##############################
### Quality of a hierarchy ###
##############################

# Normalized Dasgupta cost function
def normalized_dasgupta_cost(G, D):
    F = G.copy()
    n = F.number_of_nodes()

    # index nodes from 0 to n - 1
    if set(F.nodes()) != set(range(n)):
        F = nx.convert_node_labels_to_integers(F)

    # node weights
    w = {u: 0 for u in F.nodes()}
    wtot = 0
    for (u, v) in F.edges():
        if "weight" not in F[u][v]:
            F[u][v]["weight"] = 1
        weight = F[u][v]["weight"]
        w[u] += weight
        w[v] += weight
        wtot += weight
        if u != v:
            wtot += weight
    q = {u: 1.0 / n for u in F.nodes()}
    wtot = wtot / 2
    # aggregate graph
    H = F.copy()
    J = 0
    for t in range(n - 1):
        u = int(D[t][0])
        v = int(D[t][1])
        try:
            p = 1.0 * H[u][v]["weight"] / wtot
            J += p * (q[u] + q[v])
        except:
            pass
        H.add_node(n + t)
        neighbors_u = list(H.neighbors(u))
        neighbors_v = list(H.neighbors(v))
        for x in neighbors_u:
            H.add_edge(n + t, x, weight=H[u][x]["weight"])
        neighbors = list(H.neighbors(v))
        for x in neighbors_v:
            if H.has_edge(n + t, x):
                H[n + t][x]["weight"] += H[v][x]["weight"]
            else:
                H.add_edge(n + t, x, weight=H[v][x]["weight"])
        H.remove_node(u)
        H.remove_node(v)
        q[n + t] = q.pop(u) + q.pop(v)
    return J


###########################################
### Hierarchical Stochastic Block Model ###
###########################################

# Hierarchical Stochastic Block Model
class hsbm:
    def __init__(self, numbers, intensities):
        self._intensities = intensities
        self._numbers = numbers
        self._mus = {i: np.prod(intensities[i:]) for i in range(0, len(intensities))}
        size = np.prod(numbers)
        self._matrix = self._mus[0] * np.ones((size, size))
        for l in range(1, len(self._mus)):
            for b in range(np.prod(numbers[:l])):
                size_l = size // np.prod(numbers[:l])
                self._matrix[
                    b * size_l : (b + 1) * size_l, b * size_l : (b + 1) * size_l
                ] = self._mus[l] * np.ones((size_l, size_l))

    def create_graph(self):
        G = nx.Graph()
        for i in range(np.shape(self._matrix)[0]):
            for j in range(i):
                weight = np.random.poisson(self._matrix[i][j])
                if weight > 0 and i != j:
                    G.add_edge(i, j, weight=weight)
        return G


# ####################################
# ### Resolution analysis function ###
# ####################################

# # Perform the resolution analysis
# def resolution_analysis(G, resolutions):
#     resolution_range = np.logspace(np.log10(resolutions[-1]), np.log10(resolutions[0]), num = 100)

#     plt.figure(figsize = (8,4))
#     plt.rcParams.update({'font.size': 16})
#     plt.ylim(ymin=0, ymax=len(resolutions))
#     plt.xlabel('Resolution')
#     plt.ylabel('Number of clusters')
#     plt.step(list(reversed(resolutions)), range(len(resolutions)), 'r')
#     plt.xscale('log')

#     for r in resolutions:
#         plt.axvline(x = r, color='k', alpha=.2)
#     plt.show()

#     plt.figure(figsize = (8,4))
#     plt.ylim(ymin=0, ymax=len(resolutions))
#     plt.xlabel('Resolution')
#     plt.ylabel('Number of clusters')
#     nb_clusters = []
#     resolution_list = []
#     nb_old = 0
#     for r in resolution_range:
#         cluster = louvain(G, resolution = r)
#         nb = len(cluster)
#         nb_clusters.append(nb)
#         if nb > nb_old:
#             nb_old = nb
#             resolution_list.append(r)
#     plt.plot(resolution_range,nb_clusters, 'r+')

#     for r in resolution_list:
#         if r < resolutions[1]:
#             plt.axvline(x = r, color='k', alpha=.2)
#     plt.xscale('log')
#     plt.show()

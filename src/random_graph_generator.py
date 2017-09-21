"""
Author: Deepak Gujraniya
email: deepakgujraniya@gmail.com
"""


import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


class GenerateGraph(object):
    def __init__(self, n, p, D, graph_type="random"):
        self.graph = nx.Graph()
        nodes = self.generate_nodes(n, D)
        # for node in nodes:
        #     self.graph.add_node(node, Position=(random.randrange(0, 100), random.randrange(0, 100)))

        if graph_type == "random":
            # self.graph.add_nodes_from(nodes)
            G = nx.gnp_random_graph(n, p)
            edges = list()
            for edge in G.edges_iter():
                a, b = edge
                edges.append((nodes[a], nodes[b]))
            self.graph.add_edges_from(edges)
            # self.draw_graph()

        elif graph_type == "star_star":
            num_main_branches = n/10
            center_node = random.choice(nodes)
            # print "cetner noe", center_node
            first_level_nodes = set()
            for i in range(1, 2 * num_main_branches):
                nn = random.choice(nodes)
                if nn != center_node:
                    first_level_nodes.add(nn)
                if len(first_level_nodes) == num_main_branches:
                    break
            leaf_nodes = list(set(nodes).difference(first_level_nodes))
            print len(first_level_nodes)
            # print "leaf nodes", len(leaf_nodes)
            # G = nx.empty_graph(n)
            # add center star
            self.graph.add_star([center_node] + list(first_level_nodes))
            max_node_in_subtree = len(nodes)/len(first_level_nodes)
            i = 0
            for node in first_level_nodes:
                sub_degree = random.randint(5, max_node_in_subtree+1)
                self.graph.add_star([node] + leaf_nodes[i:sub_degree])
                i += sub_degree

            if i < len(leaf_nodes):
                self.graph.add_star([random.choice(list(first_level_nodes))] + leaf_nodes[i:])

        for nn in self.graph.nodes_iter():
            self.graph.node[nn]["Position"] = (random.randrange(0, 100), random.randrange(0, 100))


    def generate_nodes(self, n, D):
        nodes = list()
        visibility = np.abs(np.random.normal(5, 5, size=n))
        visibility = visibility/max(visibility)
        opr = np.abs(np.random.normal(0, 1, size=n))
        opr = opr / max(opr)
        true_val = np.abs(np.random.normal(0, 1, size=n))
        true_val = true_val / max(true_val)
        for i in range(n):
            d = True if i in D else False
            nodes.append(Node(i, visibility[i], opr[i], d, true_val[i]))
        return nodes

    def centrality(self):
        # print "sending centrality"
        return nx.degree_centrality(self.graph)

    def get_node(self, index):
        return [x for x in self.graph.nodes() if x.index == index][0]

    def draw_graph(self):
        nx.draw(self.graph, pos=nx.get_node_attributes(self.graph, 'Position'))
        plt.show()


class Node(object):
    def __init__(self, index, v, opr, D, value):
        self.index = index
        self.visibility = v
        self.operability = opr
        self.isDeception = D
        self.TrueValue = value


if __name__ == "__main__":
    G = GenerateGraph(500, 0.4, [2, 4], graph_type="star_star")
    # G = GenerateGraph(100, 0.4, [2, 4], graph_type="random")

    # print G.graph.nodes()
    # print G.graph.edges()
    # print "neighbors", G.graph.neighbors(G.get_node(1))
    # print s
    degree = nx.degree_centrality(G.graph)
    # print degree, "degree"
    nx.draw(G.graph)
    plt.show()
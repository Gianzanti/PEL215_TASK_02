import sys
import math
from icecream import ic


class Graph(object):
    def __init__(self, nodes: list[str], init_graph: dict[str, dict[str, float]]):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(
        self, nodes: list[str], init_graph: dict[str, dict[str, float]]
    ):
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        return graph

    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes

    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if not math.isnan(self.graph[node].get(out_node, float("NaN"))):
                connections.append(out_node)
        return connections

    def value(self, node1: str, node2: str) -> float:
        "Returns the value of an edge between two nodes."
        val = self.graph[node1].get(node2, float("NaN"))
        if math.isnan(val):
            raise Exception(
                f"Edge between {node1} and {node2} does not exist in the graph."
            )
        return val

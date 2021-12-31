import random
import time
import DiGraph
import GraphAlgo
import DiGraph
from src import Node


def GenerateRandomGraph(nodesize: int, edgesize: int) -> DiGraph.DiGraph:
    graph = DiGraph.DiGraph()
    locationkeeper = {}
    for i in range(0, nodesize):
        x = random.uniform(0, 800)
        y = random.uniform(0, 600)
        while x in locationkeeper and locationkeeper[x] == y:
            x = random.uniform(0, 800)
            y = random.uniform(0, 600)
        graph.add_node(i,(x, y, random.uniform(0, 1000)))  # Z value doesn't matter, so we don't bother checking for duplicates
    for i in range(0, edgesize):
        src = random.randint(0, nodesize-1)
        dest = random.randint(0, nodesize-1)
        destnode = graph.nodelist[dest]
        while src in destnode.inconnected:
            src = random.randint(0, nodesize-1)
            dest = random.randint(0, nodesize-1)
            destnode = graph.nodelist[dest]
        graph.add_edge(src, dest, random.uniform(0, 100))
    return graph


def main():
    # graph = GenerateRandomGraph(10000, 100000)
    algo = GraphAlgo.GraphAlgo()
    algo.load_from_json("../data/A0.json")
    algo.plot_graph()


if __name__ == '__main__':
    main()



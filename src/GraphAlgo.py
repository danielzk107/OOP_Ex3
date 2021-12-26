import array
import json
import sys
from queue import PriorityQueue
from typing import List
from src import Node
from src import Edge
from src import DiGraph


class GraphAlgo:
    """This abstract class represents an interface of a graph."""

    def __init__(self, graph: DiGraph.DiGraph):
        self.graph = graph
        self.SPDistList = {}
        self.ranSPD = False

    def get_graph(self) -> DiGraph:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            temp = open(file_name, 'r')
            jsonfile = json.load(temp)
            for x in jsonfile["Nodes"]:
                pos = str(x["pos"])
                posarray = tuple(pos.split(","))
                self.graph.add_node(x["id"], posarray)
            for x in jsonfile["Edges"]:
                id1 = int(str(x["src"]))
                id2 = int(str(x["dest"]))
                self.graph.add_edge(id1, id2, x["w"])
        except FileNotFoundError:
            raise Exception("File not found")
        except TypeError:
            raise Exception("The given file is not formatted correctly")
        except Exception:
            raise Exception("Unknown problem arose")
        return True

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name) as newfile:
                json.dump(self.graph.edgelist, newfile)
                json.dump(self.graph.nodelist, newfile)
        except FileExistsError:
            raise Exception("File already exists")
        except Exception:
            raise Exception("Unknown problem arose")
        return True

    def shortest_path_dist(self, id1: int, id2: int) -> float:
        if self.ranSPD:
            if self.SPDistList[id1, id2] < 0 or self.SPDistList[id1, id2] >= sys.float_info.max / 2:
                return -1
            return self.SPDistList[id1, id2]
        self.ranSPD = True
        # Setting all the values to the max num/to the weight of the edge:
        for x in self.graph.nodelist:
            for y in self.graph.nodelist:
                if y.idnum in x.outedgelist:
                    self.SPDistList[x, y] = x.outedgelist[y].weight
                else:
                    self.SPDistList[x, y] = sys.float_info.max / 2
        # Finding the best path for each two nodes:
        for x in self.graph.nodelist:
            for y in self.graph.nodelist:
                for z in self.graph.nodelist:
                    if self.SPDistList[y, z] > self.SPDistList[y, x] + self.SPDistList[x, z]:
                        self.SPDistList[y, z] = self.SPDistList[y, x] + self.SPDistList[x, z]
        return self.SPDistList[id1, id2]

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        visited = list()
        parent = {}
        pq = PriorityQueue()
        dist = {x: float('inf') for x in self.graph.nodelist}
        dist[id1] = 0
        pq.put((0, id1))
        parent[id1] = -1
        while not pq.empty():
            (x, curr) = pq.get()
            visited.append(curr)
            for neighbor in self.graph.nodelist:
                node = self.graph.nodelist[neighbor]
                if curr in node.inconnected:
                    distance = node.inedgelistbyweight[curr]
                    if node.idnum not in visited:
                        if dist[curr] + distance < dist[node.idnum]:
                            dist[node.idnum] = dist[curr] + distance
                            pq.put((dist[curr] + distance, node.idnum))
                            parent[neighbor] = curr
        if id2 not in parent:
            return float('inf'), None
        output = self.getlistofparent(id2, parent, list())
        output.reverse()
        return dist[id2], output

    def getlistofparent(self, id: int, parent: dict, l: list) -> list:
        l.append(id)
        print(id)
        if parent[id] == -1:
            return l
        return self.getlistofparent(parent[id], parent, l)
    # def shortest_path_helper(self, ):
    def DFSIn(self, a: int):
        node = self.graph.nodelist[a]
        node.tag = 1
        for x in node.inconnected:
            if self.graph.nodelist[x].tag != 1:
                self.DFSIn(x)

    def DFSOut(self, a: int):
        node = self.graph.nodelist[a]
        node.tag = 1
        for x in node.outconnected:
            if self.graph.nodelist[x].tag != 1:
                self.DFSOut(x)

    def IsConnected(self):
        self.DFSOut(0)
        for x in self.graph.nodelist:
            if x.tag != 1:
                return False
            x.tag = 0
        self.DFSIn(0)
        for x in self.graph.nodelist:
            if x.tag != 1:
                return False
            x.tag = 0
        return True

    def TSP(self, node_lst: List[int]) -> (List[int], float):

        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """

    def centerPoint(self) -> (int, float):
        if not self.IsConnected():
            return None
        maximumshortestpatharr = {}
        for x in self.graph.nodelist:
            maxdist = sys.float_info.min
            for y in self.graph.nodelist:
                if x != y:
                    if self.shortest_path_dist(x.idnum, y.idnum) > maxdist:
                        maxdist = self.shortest_path_dist(x.idnum, y.idnum)

            maximumshortestpatharr[x.idnum] = maxdist
        minimum = sys.float_info.max
        centreindex = 0
        for x in self.graph.nodelist:
            if maximumshortestpatharr[x.idnum] < minimum:
                minimum = maximumshortestpatharr[x.idnum]
                centreindex = x.idnum
        return centreindex, minimum

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        raise NotImplementedError

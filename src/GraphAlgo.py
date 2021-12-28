import json
import random
import sys
from queue import PriorityQueue
from typing import List
import DiGraph
import Node
import GUI


def Hit_Node(x: float, y: float, graph: DiGraph.DiGraph) -> (int, Node.Node):  #A function that checks if there is a node in close proximity to the given coordinates (the function will return the first node it encounters)
    for nodeid in graph.nodelist:
        node = graph.nodelist[nodeid]
        if abs(node.x - x) <= 8 and abs(node.y - y) <= 8:
            return nodeid, node
    return -1, None


class GraphAlgo:

    def __init__(self, graph = None):
        if graph is None:
            self.graph = DiGraph.DiGraph()
        else:
            self.graph = graph
        self.SPDistList = {}
        self.ranSPD = False
        self.modcount = self.graph.modcount

    def get_graph(self) -> DiGraph:
        return self.graph

    def set_graph(self, newgraph: DiGraph.DiGraph):
        self.graph = newgraph

    def load_from_json(self, file_name: str) -> bool:
        try:
            print(file_name)
            temp = open(file_name, 'r')
            jsonfile = json.load(temp)
            for x in jsonfile["Nodes"]:
                try:
                    pos = str(x["pos"])
                except KeyError:
                    pos = "0,0,-1"  # making z -1 to distinguish between position-less nodes and nodes with position (0,0)
                posarray = tuple(pos.split(","))
                self.graph.add_node(x["id"], posarray)
            for x in jsonfile["Edges"]:
                id1 = int(str(x["src"]))
                id2 = int(str(x["dest"]))
                self.graph.add_edge(id1, id2, x["w"])
        except FileNotFoundError:
            temp.close()
            raise Exception("File not found")
        except TypeError:
            temp.close()
            raise Exception("The given file is not formatted correctly")
        except Exception:
            temp.close()
            raise Exception("Unknown problem arose")
        temp.close()
        return True

    def save_to_json(self, file_name: str) -> bool:
        try:
            temp = open(file_name, 'r')
            print("File already exists")
            temp.close()
            return False
        except FileNotFoundError:
            try:
                with open(file_name, 'w', newline="") as newfile:
                    nodeslist = list()
                    for x in self.graph.nodelist:
                        pos = (self.graph.nodelist[x].x, self.graph.nodelist[x].y, self.graph.nodelist[x].z).__str__()
                        temp = pos.replace("(", "")
                        newpos = temp.replace(")", "")
                        nodeslist.append({"id": self.graph.nodelist[x].idnum, "pos": newpos})
                    edgeslist = list()
                    for x in self.graph.edgelist:
                        edgeslist.append({"src": self.graph.edgelist[x].src, "dest": self.graph.edgelist[x].dest,
                                          "w": self.graph.edgelist[x].weight})
                    json.dump({"Nodes": nodeslist, "Edges": edgeslist}, newfile, indent=4)
            except FileExistsError:
                raise Exception("File already exists")
            except Exception:
                newfile.close()
                raise Exception("Unknown problem arose")
            newfile.close()
            return True

    def shortest_path_dist(self, id1: int, id2: int) -> float:
        if id1 == id2:
            return float('inf')
        if self.ranSPD and self.modcount == self.graph.modcount:
            if self.SPDistList[id1, id2] < 0 or self.SPDistList[id1, id2] >= sys.float_info.max / 2:
                return float('inf')
            return self.SPDistList[id1, id2]
        self.ranSPD = True
        self.modcount = self.graph.modcount
        # Setting all the values to the max num/to the weight of the edge:
        for x in self.graph.nodelist:
            xnode = self.graph.nodelist[x]
            for y in self.graph.nodelist:
                if y in xnode.outedgelist:
                    self.SPDistList[x, y] = xnode.outedgelist[y].weight
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
        # Simple Dijkstra's algorithm
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
                if curr in node.inedgelistbyweight:
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

    def getlistofparent(self, idnum: int, parent: dict, l: list) -> list:
        node = self.graph.nodelist[idnum]
        node.tag = 1
        l.append(idnum)
        if parent[idnum] == -1:
            return l
        return self.getlistofparent(parent[idnum], parent, l)

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
        for nodeid in self.graph.nodelist:
            node = self.graph.nodelist[nodeid]
            node.tag = 0
        num = float('inf')
        for x in self.graph.nodelist:  # Making sure we run the DFS functions on a real node in the graph
            num = x
        if num == float('inf'):
            print("Graph is empty")
            return False
        self.DFSOut(num)
        for x in self.graph.nodelist:
            node = self.graph.nodelist[x]
            if node.tag != 1:
                return False
            node.tag = 0
        self.DFSIn(num)
        for x in self.graph.nodelist:
            node = self.graph.nodelist[x]
            if node.tag != 1:
                return False
            node.tag = 0
        return True

    def TSP(self, node_list: List[int]) -> (List[int], float):
        output_list = list()
        output_dist = 0
        for nodeid in node_list:
            node = self.graph.nodelist[nodeid]
            node.tag = 0
        for nodeid in node_list:
            if nodeid in output_list and output_list[len(output_list) - 1] != nodeid:
                continue
            closest = nodeid
            for othernodeid in node_list:
                if self.shortest_path_dist(nodeid, othernodeid) < self.shortest_path_dist(nodeid, closest):
                    closest = othernodeid
            dist, path = self.shortest_path(nodeid, closest)
            output_list.extend(path)
            output_dist += dist
            visitedall = True
            for x in node_list:
                node = self.graph.nodelist[x]
                if node.tag != 1:
                    visitedall = False
                    break
            if visitedall:
                break
        return output_list, output_dist

    def centerPoint(self) -> (int, float):
        if not self.IsConnected():
            return None
        maximumshortestpatharr = {}
        for x in self.graph.nodelist:
            maxdist = sys.float_info.min
            for y in self.graph.nodelist:
                if x != y:
                    if self.shortest_path_dist(x, y) > maxdist:
                        maxdist = self.shortest_path_dist(x, y)
            maximumshortestpatharr[x] = maxdist
        minimum = sys.float_info.max
        centreindex = 0
        for x in self.graph.nodelist:
            if maximumshortestpatharr[x] < minimum:
                minimum = maximumshortestpatharr[x]
                centreindex = x
        return centreindex, minimum

    def plot_graph(self) -> None:
        gui = GUI.GUI(self.GetfixedGraph(), self)
        gui.PrintGraph()

    def xAndyDiff(self) -> (float, float):
        x = y = 0
        for node1 in self.graph.nodelist:
            for node2 in self.graph.nodelist:
                if abs((self.graph.nodelist[node2].x - self.graph.nodelist[node1].x)) > x:
                    x = abs((self.graph.nodelist[node2].x - self.graph.nodelist[node1].x))
                if abs((self.graph.nodelist[node2].y - self.graph.nodelist[node1].y)) > y:
                    y = abs((self.graph.nodelist[node2].y - self.graph.nodelist[node1].y))
        return x, y

    def GetfixedGraph(self) -> DiGraph.DiGraph:
        output = DiGraph.DiGraph()
        (xdiff, ydiff) = self.xAndyDiff()
        for n in self.graph.nodelist:
            node = self.graph.nodelist[n]
            if node.z == -1:
                output.add_node(n, (random.uniform(40, 550), random.uniform(55, 400), 0))
                continue
            x = node.x
            y = node.y
            if x == y == 0:
                y = 60
                output.add_node(n, (x, y + 50, 0))
                continue
            count = 1
            while x > xdiff:
                if x < 1:
                    x = float("0." + str(x)[3:])
                    x = x / pow(10, count)
                    count += 1
                else:
                    if float(str(x)[1:]) == 0:
                        x = x / 10.0
                    else:
                        x = float(str(x)[1:])
            count = 1
            while y > ydiff:
                if y < 1:
                    y = float("0." + str(y)[3:])
                    y = y / pow(10, count)
                    count += 1
                else:
                    if float(str(y)[1:]) == 0:
                        y = y / 10
                    else:
                        y = float(str(y)[1:])
            while x < (800 / 15):
                if x == 0:
                    break
                x *= 10
            while y < (600 / 15):
                if y == 0:
                    y = 10
                    break
                y *= 10
            output.add_node(n, (x, y + 50, 0))
        for edgeid in self.graph.edgelist:
            edge = self.graph.edgelist[edgeid]
            output.add_edge(edge.src, edge.dest, edge.weight)
        return output

import sys

import pygame
import random
from time import sleep
import DiGraph
import Node
import Edge
import GraphAlgo


class GUI:
    def __init__(self, graph: DiGraph.DiGraph, algo: GraphAlgo):
        self.graph = graph
        self.algo = algo
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont('David', 17)
        self.shortest_path_text = self.font.render("Shortest path", True, (255, 255, 255))
        self.centre_text = self.font.render("Show centre", True, (255, 255, 255))
        self.add_node_text = self.font.render("Add node", True, (255, 255, 255))
        self.add_edge_text = self.font.render("Add edge", True, (255, 255, 255))
        self.save_text = self.font.render("Save", True, (255, 255, 255))
        self.centre = -1

    def PrintGraph(self):
        pygame.display.set_caption("Gradually Graining Graph Grouper")
        shortestpathclicked = False
        running = True
        self.screen.fill((67, 212, 164))
        for edgeid in self.graph.edgelist:
            self.Draw_Edge(self.graph.edgelist[edgeid])
        for nodeid in self.graph.nodelist:
            self.Draw_node(self.graph.nodelist[nodeid])
        pygame.draw.rect(self.screen, pygame.color.Color((0, 0, 0)), pygame.Rect(0.0, 0.0, 800, 50), 1, 1, 1, 1, 1, 1)
        self.Refresh_Topof_Screen()
        pygame.display.update()
        path = None
        firstnode = secondnode = -1
        while running:
            for event in pygame.event.get():
                self.add_node_text = self.font.render("Add node", True, (255, 255, 255))
                self.Refresh_Topof_Screen()
                if event.type == pygame.QUIT:
                    final_display_text2 = self.font.render("Thank you for using this software, goodbye!", True, (255, 255, 255))
                    self.screen.blit(final_display_text2, (400, 300))
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (nodeid, node) = GraphAlgo.Hit_Node(mouse[0], mouse[1], self.graph)
                    if shortestpathclicked and node is not None:
                        self.Refresh_Topof_Screen()
                        if firstnode == -1:
                            firstnode = nodeid
                        else:
                            if secondnode == -1:
                                secondnode = nodeid
                                shortestpathclicked = False
                        if not shortestpathclicked:
                            (length, path) = self.algo.shortest_path(firstnode, secondnode)
                            if length == float('inf'):
                                self.shortest_path_text = self.font.render("There is no path from " + str(firstnode) + " to " + str(secondnode), True, (255, 255, 255))
                            else:
                                format_length = "{:.3f}".format(length)
                                self.HighlightPath(path)
                                self.shortest_path_text = self.font.render("Displaying the path from " + str(firstnode) + " to " + str(secondnode) + ": " + str(format_length), True, (255, 255, 255))
                            self.Refresh_Topof_Screen()
                            firstnode = secondnode = -1
                        else:
                            self.shortest_path_text = self.font.render("Picked node number " + str(nodeid), True, (255, 255, 255))
                            self.Refresh_Topof_Screen()
                    if 30 <= mouse[0] <= 230 and 0 <= mouse[1] <= 50 and not shortestpathclicked:
                        if path is not None:
                            self.Un_HighlightPath(path)
                        self.shortest_path_text = self.font.render("Please choose two nodes", True, (255, 255, 255))
                        self.Refresh_Topof_Screen()
                        shortestpathclicked = True
                    if 305 <= mouse[0] <= 440 and 0 <= mouse[1] <= 50:  # Centre button clicked
                        try:
                            (centrenodeid, throwaway) = self.algo.centerPoint()
                            if centrenodeid is None:
                                self.centre_text = self.font.render("Graph not connected", True, (255, 255, 255))
                            else:
                                if self.centre != -1 and self.centre != centrenodeid:
                                    centrenode = self.graph.nodelist[self.centre]
                                    pygame.draw.circle(self.screen, pygame.color.Color((67, 212, 164)), (centrenode.x, centrenode.y), 4)
                                    self.Draw_node(centrenode)
                                self.centre = centrenodeid
                                centrenode = self.graph.nodelist[centrenodeid]
                                self.centre_text = self.font.render("The centre node is " + str(centrenodeid), True, (255, 255, 255))
                                pygame.draw.circle(self.screen, pygame.color.Color((86, 164, 233)), (centrenode.x, centrenode.y), 4)
                            self.Refresh_Topof_Screen()
                        except TypeError:
                            self.centre_text = self.font.render("Graph not connected", True, (255, 255, 255))
                            self.Refresh_Topof_Screen()
                    if 480 <= mouse[0] <= 560 and 0 <= mouse[1] <= 50:  # Add_node button clicked
                        self.Add_Node_Action()
                    if 600 <= mouse[0] <= 700 and 0 <= mouse[1] <= 50:  # Add_edge button clicked
                        self.Add_Edge_Action()
                    if 705 <= mouse[0] and 0 <= mouse[1] <= 50:  # Save button clicked
                        num = random.randint(0, 1000)
                        condition = self.algo.save_to_json("Graph" + str(num) + ".json")
                        while not condition:
                            num = random.randint(0, 1000)
                            condition = self.algo.save_to_json("Graph" + str(num) + ".json")
                        final_display_text1 = self.font.render("Graph saved as Graph" + str(num) + ".json", True, (255, 255, 255))
                        final_display_text2 = self.font.render("Thank you for using this software, goodbye!", True, (255, 255, 255))
                        self.screen.blit(final_display_text1, (400, 250))
                        self.screen.blit(final_display_text2, (400, 300))
                        running = False
            mouse = pygame.mouse.get_pos()
            pygame.display.update()
        sleep(1)

    def HighlightPath(self, path: list):
        for i in range(0, len(path) - 1):
            last = self.graph.nodelist[path[i]]
            curr = self.graph.nodelist[path[i + 1]]
            pygame.draw.line(self.screen, pygame.color.Color((233, 86, 86)), (last.x, last.y), (curr.x, curr.y), 2)

    def Un_HighlightPath(self, path: list):
        for i in range(0, len(path) - 1):
            last = self.graph.nodelist[path[i]]
            curr = self.graph.nodelist[path[i + 1]]
            pygame.draw.line(self.screen, pygame.color.Color((210, 223, 94)), (last.x, last.y), (curr.x, curr.y), 2)

    def Draw_node(self, node: Node.Node):
        pygame.draw.circle(self.screen, pygame.color.Color((228, 164, 68)), (node.x, node.y), 2)

    def Draw_Edge(self, edge: Edge.Edge):
        pygame.draw.line(self.screen, pygame.color.Color((210, 223, 94)),
                         (self.graph.nodelist[edge.src].x, self.graph.nodelist[edge.src].y),
                         (self.graph.nodelist[edge.dest].x, self.graph.nodelist[edge.dest].y), 2)

    def Refresh_Topof_Screen(self):
        self.screen.fill((67, 212, 164), (0.0, 0.0, 800, 50))
        pygame.draw.rect(self.screen, pygame.color.Color((0, 0, 0)), pygame.Rect(0.0, 0.0, 800, 50), 1, 1, 1, 1, 1, 1)
        self.screen.blit(self.shortest_path_text, (20, 20))
        self.screen.blit(self.centre_text, (305, 20))
        self.screen.blit(self.add_node_text, (490, 20))
        self.screen.blit(self.add_edge_text, (600, 20))
        self.screen.blit(self.save_text, (705, 20))

    def Add_Edge_Action(self):
        condition = True
        self.add_edge_text = self.font.render("Choose nodes", True, (255, 255, 255))
        self.Refresh_Topof_Screen()
        node1 = node2 = None
        while condition:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (nodeid, node) = GraphAlgo.Hit_Node(mouse[0], mouse[1], self.graph)
                    if node is not None:
                        print("Selected node " + str(nodeid))
                        if node1 is None:
                            node1 = node
                        else:
                            if node2 is None:
                                node2 = node
                                if node2.idnum in node1.outedgelist:
                                    self.add_edge_text = self.font.render("Edge exists", True, (255, 255, 255))
                                    condition = False
                                    self.Refresh_Topof_Screen()
                                    return
                                self.graph.add_edge(node1.idnum, node2.idnum, 1)
                                self.algo.graph.add_edge(node1.idnum, node2.idnum, 1)
                                self.Draw_Edge(Edge.Edge(node1.idnum, node2.idnum, 1, 2))
                                self.add_edge_text = self.font.render("Edge added", True, (255, 255, 255))
                                condition = False
                                self.Refresh_Topof_Screen()
                                return
                            else:
                                self.graph.add_edge(node1.idnum, node2.idnum, 1)
                                self.algo.graph.add_edge(node1.idnum, node2.idnum, 1)
                                self.Draw_Edge(Edge.Edge(node1.idnum, node2.idnum, 1, 2))
                                self.add_edge_text = self.font.render("Edge added", True, (255, 255, 255))
                                condition = False
                                self.Refresh_Topof_Screen()
                                return
                    else:
                        self.add_edge_text = self.font.render("None selected", True, (255, 255, 255))
                        condition = False
                        self.Refresh_Topof_Screen()
                        return

    def Add_Node_Action(self):
        condition = True
        self.add_node_text = self.font.render("Choose place", True, (255, 255, 255))
        self.Refresh_Topof_Screen()
        while condition:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (nodeid, node) = GraphAlgo.Hit_Node(mouse[0], mouse[1], self.graph)
                    if node is not None:
                        self.add_node_text = self.font.render("Place taken", True, (255, 255, 255))
                    else:
                        if mouse[1] < 60:
                            self.add_node_text = self.font.render("Try again", True, (255, 255, 255))
                        else:
                            self.graph.add_node(self.graph.size, (mouse[0], mouse[1], 0))
                            node = Node.Node(self.graph.size, mouse[0], mouse[1], 0)
                            self.Add_Node_To_Graph(node)
                            self.Draw_node(node)
                            self.add_node_text = self.font.render("Node Added", True, (255, 255, 255))
                    condition = False
                    self.Refresh_Topof_Screen()
                    return

    def Add_Node_To_Graph(self, node: Node.Node):
        maxx = sys.float_info.min
        minx = sys.float_info.max
        maxy = sys.float_info.min
        miny = sys.float_info.max
        for nodeid in self.algo.graph.nodelist:
            node = self.algo.graph.nodelist[nodeid]
            miny = min(node.y, miny)
            maxy = max(node.y, maxy)
            minx = min(node.x, minx)
            maxx = max(node.x, maxx)
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        if not self.algo.graph.add_node(self.algo.graph.size, (x, y, 0)):
            print("A")

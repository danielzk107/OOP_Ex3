import pygame
from src import DiGraph
from src import Node
from src import Edge
from src import GraphAlgo

class GUI:
    def __init__(self, graph: DiGraph.DiGraph, algo: GraphAlgo.GraphAlgo):
        self.graph = graph
        self.algo = algo
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

    def PrintGraph(self):
        pygame.display.set_caption("Gradually Graining Graph Grouper")
        font = pygame.font.SysFont('David', 17)
        shortest_path_text = font.render("Shortest path", True, (255, 255, 255))
        centre_text = font.render("Show centre", True, (255, 255, 255))
        add_node_text = font.render("Add node", True, (255, 255, 255))
        add_edge_text = font.render("Add edge", True, (255, 255, 255))
        shortestpathclicked = False
        running = True
        self.screen.fill((67, 212, 164))
        for edgeid in self.graph.edgelist:
            self.Draw_Edge(self.graph.edgelist[edgeid])
        for nodeid in self.graph.nodelist:
            self.Draw_node(self.graph.nodelist[nodeid])
        pygame.draw.rect(self.screen, pygame.color.Color((0, 0, 0)), pygame.Rect(0.0, 0.0, 800, 50), 1, 1, 1, 1, 1, 1)
        self.screen.blit(shortest_path_text, (20, 20))
        self.screen.blit(centre_text, (340, 20))
        self.screen.blit(add_node_text, (490, 20))
        self.screen.blit(add_edge_text, (600, 20))
        pygame.display.update()
        path = None
        firstnode = secondnode = -1
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (nodeid, node) = GraphAlgo.Hit_Node(mouse[0], mouse[1], self.graph)
                    print(mouse[0], mouse[1])
                    if shortestpathclicked and node is not None:
                        self.screen.fill((67, 212, 164), (0.0, 0.0, 800, 50))
                        pygame.draw.rect(self.screen, pygame.color.Color((0, 0, 0)), pygame.Rect(0.0, 0.0, 800, 50), 1, 1, 1, 1, 1, 1)
                        self.screen.blit(centre_text, (340, 20))
                        if firstnode == -1:
                            firstnode = nodeid
                        else:
                            if secondnode == -1:
                                secondnode = nodeid
                                shortestpathclicked = False
                        if not shortestpathclicked:
                            (length, path) = self.algo.shortest_path(firstnode, secondnode)
                            if length == float('inf'):
                                shortest_path_text = font.render(
                                    "There is no path from " + str(firstnode) + " to " + str(secondnode), True,
                                    (255, 255, 255))
                            else:
                                format_length = "{:.3f}".format(length)
                                self.HighlightPath(path)
                                shortest_path_text = font.render(
                                    "Displaying the path from " + str(firstnode) + " to " + str(secondnode) + ": " + str(format_length), True, (255, 255, 255))
                            self.screen.blit(shortest_path_text, (20, 20))
                            firstnode = secondnode = -1
                        else:
                            shortest_path_text = font.render("Picked node number " + str(nodeid), True, (255, 255, 255))
                            self.screen.blit(shortest_path_text, (20, 20))
                    if 30 <= mouse[0] <= 230 and 0 <= mouse[1] <= 50 and not shortestpathclicked:
                        if path is not None:
                            self.Un_HighlightPath(path)
                        self.screen.fill((67, 212, 164), (0.0, 0.0, 800, 50))
                        pygame.draw.rect(self.screen, pygame.color.Color((0, 0, 0)), pygame.Rect(0.0, 0.0, 800, 50), 1, 1, 1,
                                         1, 1, 1)
                        self.screen.blit(centre_text, (340, 20))
                        shortest_path_text = font.render("Please choose two nodes", True, (255, 255, 255))
                        self.screen.blit(shortest_path_text, (20, 20))
                        print("Hi")
                        shortestpathclicked = True
                    if 340 <= mouse[0] <= 440 and 0 <= mouse[1] <= 50:
                        self.screen.fill((67, 212, 164), (340, 1, 800, 48))
                        (centrenodeid, throwaway) = self.algo.centerPoint()
                        if centrenodeid is None:
                            centre_text = font.render("The graph isn't connected", True, (255, 255, 255))
                        else:
                            centrenode = self.graph.nodelist[centrenodeid]
                            centre_text = font.render("The centre node is " + str(centrenodeid), True, (255, 255, 255))
                            pygame.draw.circle(self.screen, pygame.color.Color((86, 164, 233)), (centrenode.x, centrenode.y), 4)
                        self.screen.blit(centre_text, (340, 20))

                    # print(mouse[0], mouse[1])
            mouse = pygame.mouse.get_pos()
            pygame.display.update()

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


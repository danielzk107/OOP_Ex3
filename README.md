# OOP_Ex3
(Disclaimer: during this readme file i mention "we" quite a few times. That is purely for aesthetic and readability reasons, as this assignment was done by myself alone.)

This project is the fourth assignment in the course "Object Oriented Programming". Like the third assignment, this project is about implementing an api of directed weighted graphs and algorithms regarding them. While the last assignment was written in Java, this one is written in Python. [Here](https://github.com/danielzk107/OOP_Ex2) is a link to the previous project. In this README file, we will provide a short explanation for each of the objects and show how we implemented their interfaces, as well as give instructions as to how one can download and run the program. to skip to the explanation of how to install and run the program, click [here](https://github.com/danielzk107/OOP_Ex3#how-to-run)

## Implementation

Python is infamous for its inneficiency and general "slowness", so here efficient implementation is even more important than in the previous project. Again, every class was written with that in mind, and so we have used efficient data structures for every one of our classes, and used dynamic programming whenever possible.

### Node

The node class in this project is practically identical to the one in the previous one, except this implementation uses dictionaries instead of Hashmaps (dictionaries are the Python equivalent). this class has two basic functions; one to add an edge and one to remove it. the dictionaries in this class are, of course, used to maximize efficiency, since they are housing all the adjacent nodes and edges (the neighbors) of the node.

### DiGraph

The Digraph class is relatively simplistic; It uses two dictionaries to represent its nodes and edges, has one modcount variable to keep track of the number of changes that have been done to the object, and a size variable for the sake of comfort and code readability. This class has four functions that aren't trivial (that is, four functions that aren't simply one or two lines), and they are very simple: one function to add a node to the graph, one to remove a node, one to add an edge, and one to remove an edge. The only function that might prove to be tricky is the removal of a node, since all the edges connected to said node would have to be removed as well. that is solved by our implementation os the Node class, which keeps dictionaries of all the other nodes and edges connected to itself. 

### GraphAlgo

The GraphAlgo class is the class that preforms all the different algorithms used on Directed Weighted graphs (at least, all the algorithms requested to implement). In terms of variables, this class has four; The graph it operates on, a modcount which would be compared to the graph's modcount, a dictionary which keeps the distance between every two nodes, and a boolean variable which keeps track of whether the function that finds the distance between all the nodes has been run or not. the functions of this class are:

#### load_from_json and save_to_json

The load function tries to locate a json file with the given name and create a new graph with all the variables written inside that json file. since there are many possible ways for the program to crash inside functions that work with json file, both these functions work using try/except and throw errors when the given filename doesn't exists (in the case of the loading function) or when it does (in the case of the save function), and when the file is not formatted correctly. The save function is simpler than the load function, as all it does it transfer the graph's variable into lists and "dumps" them inside the json file it opened.

#### shortest_path_dist

This function isn't requested in the api, but it is crucial if one wants to use the centrenode function on a larger graph. This function is simply the Floyd-Warshal algorithm to find the shortest path between every two nodes, but it keep all the distances inside the variable "SPDistList". once the function has been run once it changes the variable ranSPD to true, so the next time that it is called (if the modecount of the objact is the same as the modecount of its graph), it simply returns the value of SPDistList[id1, id2] (when id1 is the first node and id2 is the second).

#### shortest_path

This function is simply dijkstra's algorithm to find the sortest path between two given nodes. It uses a helper function (getlistofparent) to get the actual path between the two given nodes and returns both the path and the distance.

#### IsConnected

This functions checks if the graph is connected or not. It does so using recursion and two DFS helper functions (becuase the function uses recursion, it cant be run on very large graphs, becuase of the maximum recursion depth that most compilers have). First, the tags of all nodes are set to 0. Then, the program runs the function DFSOut on the first node in the graph to check if all the other nodes are reachable through that node (the DFS functions changes the tags of all the nodes it reaches to 1). The, the tags of all the nodes are set to 0, the DFSIn function is called, and we check if the first node is reachable from all other nodes.

#### centrenode

This function will only work on a graph that is connected, so it first checks if it is. If the graph is indeed connected, the function checks for each node what the furthest distance is to another node. then, it picks the node which is closest to its furthest node (the node which has the minimal furthest distance to another) and returns it and the furthest distance from it to another.

### Testing

This project has two testing files: TestDiGraph and TestGraphAlgo, which test DiGraph and GraphAlgo respectively. The testing is done using unittest and comparing between the given results and the known values.

## GUI

The GUI for this project uses Pygame, which is a free open source Python GUI. the GUI itself is vey basic; it displays a window with a visual representation of the graph and some buttons that give you the option to add a node or an edge, find the shortest path between two nodes, find the centre of the graph, and save it to a json file.
Here is an example of it running the file "A0.json":

![Ex3_GUI](https://user-images.githubusercontent.com/92798950/147828573-87f1a04b-e66b-4c8a-b8c2-0fcdd08200a5.png)


## Performance

When working on two nearly identical projects, one has to ask themselves which one is "better". Which one is faster, or more accurate, or more applicable to the real world, and similar questions. for that reason, we have made a comparison between the perfomances of this program against the previous one:

All function were ran on a graph with the witten node size and an average of 20 connections per node (10 times more edges than nodes)

All the values written are in seconds.

Here is a table with the average runtimes for the centrenode function, which returns the centre node of the graph (if it is connected)

| Size | Java | Python |
| --- | --- | --- |
| 100 | 0.0034821 |  0.2920946 |
| 1000 | 0.089724 | 375 |
| 10000 | 4.53691 | Recursion error* |
| 100000 | heap error** | Recursion error |
| 1000000 | heap error | Recursion error |

In this table we can clearly see that the python program (this project) is significantly slower than the java program (the previous project). Because of the immense similarity between the projects, we can conclude that the python language itself is slower than java.

\* Recursion error means the program has reached maximum recursion depth

** Heap error means the program has reached its maximum capacity in terms of memory

## How To Run
This project, unlike the previous one, has no executable file. In order to run the program, first, one has to download the code and open it on a Python compiler, such as visual studio or Pycharm (other options are available). Once the project is open in a compatible compiler, open the Ex3_main.py file, where you can run any function you would like on a randomly generated graph of any size you choose. In order to load a graph from a json file, use algo.load_from_json(finlename) instead of generating a random graph. the current main function is in its testing form, so it currently displays the graph loaded from the file "A0.json".


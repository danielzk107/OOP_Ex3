# OOP_Ex3
(Disclaimer: during this readme file i mention "we" quite a few times. That is purely for aesthetic and readability reasons, as this assignment was done by myself alone.)

This project is the fourth assignment in the course "Object Oriented Programming". Like the third assignment, this project is about implementing an api of directed weighted graphs and algorithms regarding them. While the last assignment was written in Java, this one is written in Python. [Here](https://github.com/danielzk107/OOP_Ex2) is a link to the previous project. In this README file, we will provide a short explanation for each of the objects and show how we implemented their interfaces, as well as give instructions as to how one can download and run the program. to skip to the explanation of how to install and run the program, click here

## Implementation

Python is infamous for its inneficiency and general "slowness", so here efficient implementation is even more important than in the previous project. Again, every class was written with that in mind, and so we have used efficient data structures for every one of our classes, and used dynamic programming whenever possible.

### Node

The node class in this project is practically identical to the one in the previous one, except this implementation uses dictionaries instead of Hashmaps (dictionaries are the Python equivalent). this class has two basic functions; one to add an edge and one to remove it. the dictionaries in this class are, of course, used to maximize efficiency, since they are housing all the adjacent nodes and edges (the neighbors) of the node.

### DiGraph



### GraphAlgo


### Testing



## GUI


## Performance

When working on two nearly identical projects, one has to ask themselves which one is "better". Which one is faster, or more accurate, or more applicable to the real world, and similar questions. for that reason, we have made a comparison between the perfomances of this program against the previous one:

python, size: 1000, find centre: 375 secs



## How To Run



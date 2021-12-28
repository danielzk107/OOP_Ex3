import unittest
import GraphAlgo


class Tests(unittest.TestCase):

    def main(self):
        algo = GraphAlgo.GraphAlgo()
        algo.load_from_json("../data/A5.json")
        self.shortest_path_test(algo)

    def shortest_path_test(self, algo: GraphAlgo.GraphAlgo):
        self.assertEqual(algo.shortest_path(1, 25), (8.799105214730114, [1, 9, 11, 13, 14, 15, 16, 25]))
        self.assertEqual(algo.shortest_path(4, 37), (4.711279260413576, [4, 13, 14, 38, 37]))


if __name__ == '__main__':
    Tests.main()

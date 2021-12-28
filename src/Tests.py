import unittest
import GraphAlgo


class Tests(unittest.TestCase):

    def test_shortest_path(self):
        algo = GraphAlgo.GraphAlgo()
        algo.load_from_json("../data/A5.json")
        self.assertEqual(algo.shortest_path(1, 25), (8.799105214730114, [1, 9, 11, 13, 14, 15, 16, 25]))
        self.assertEqual(algo.shortest_path(4, 37), (4.711279260413576, [4, 13, 14, 38, 37]))
        self.assertEqual(algo.shortest_path(0, 0), (0, [0]))
        self.assertEqual(algo.shortest_path(2, 66), (float('inf'), None))
        self.assertEqual(algo.shortest_path(42, 12), (9.89827933470553, [42, 41, 40, 39, 15, 14, 13, 12]))
        algo = GraphAlgo.GraphAlgo()
        algo.load_from_json("../data/T0.json")
        self.assertEqual(algo.shortest_path(2, 66), (float('inf'), None))
        self.assertEqual(algo.shortest_path(1, 2), (1.3, [1, 2]))
        self.assertEqual(algo.shortest_path(1, 3), (1.8, [1, 3]))
        self.assertEqual(algo.shortest_path(0, 3), (2.8, [0, 1, 3]))

    def test_centre(self):
        algo = GraphAlgo.GraphAlgo()
        algo.load_from_json("../data/A0.json")
        self.assertEqual(algo.centerPoint(), (7, 6.806805834715163))
        algo.load_from_json("../data/A5.json")
        self.assertEqual(algo.centerPoint(), (40, 9.291743173960954))
        algo = GraphAlgo.GraphAlgo()
        algo.load_from_json("../data/T0.json")
        self.assertEqual(algo.centerPoint(), None)

    def test_connected(self):
        algo = GraphAlgo.GraphAlgo()
        algo.load_from_json("../data/A0.json")
        self.assertEqual(algo.IsConnected(), True)
        algo.load_from_json("../data/A5.json")
        self.assertEqual(algo.IsConnected(), True)
        algo = GraphAlgo.GraphAlgo()
        algo.load_from_json("../data/T0.json")
        self.assertEqual(algo.IsConnected(), False)


if __name__ == '__main__':
    unittest.main()

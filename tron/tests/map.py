import unittest

from tron.map import Map

class TestMap(unittest.TestCase):
    def test_constructor(self):
        mymap = Map(3, 3, 0, -1)
        for i in range(5):
            self.assertEqual(mymap._data[0][i], -1)
            self.assertEqual(mymap._data[i][0], -1)
            self.assertEqual(mymap._data[4][i], -1)
            self.assertEqual(mymap._data[i][4], -1)
        for i in range(1, 4):
            for j in range(1, 4):
                self.assertEqual(mymap._data[i][j], 0)

    def test_clone(self):
        original = Map(3, 3, 0, -1)
        mymap = Map(3, 3, 0, -1)
        mymap2 = mymap.clone()
        for i in range(5):
            for j in range(5):
                self.assertEqual(mymap._data[i][j], mymap2._data[i][j])
                mymap._data[i][j] = 3

        for i in range(5):
            for j in range(5):
                self.assertEqual(original._data[i][j], mymap2._data[i][j])

    def test_convert(self):
        def increment(x):
            return x + 1

        original = Map(3, 3, 0, -1)
        converted = original.convert(increment)

        for i in range(5):
            for j in range(5):
                self.assertEqual(converted._data[i][j], original._data[i][j] + 1)


if __name__ == '__main__':
    unittest.main()

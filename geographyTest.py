import unittest
from geography import distance, bearing, location


class TestSequenceFunctions(unittest.TestCase):
    """Test distance() functionality"""
    def setUp(self):
        self.seq = range(10)
        
                
    def test_ZeroDistance(self):
        """Distance between same points must be zero"""
        point1 = (0,0)
        dis = distance(point1,point1);
        self.assertEqual(0,dis);

    
    def test_RoundTrip(self):
        """Distance from point1 to point2 same in other direction too"""
        point1 = (0.0, 0.0)
        point2 = (0.0, 1.0)
        d1 = distance(point1,point2)
        d2 = distance(point2, point1)
        print d1, d2
        self.assertEqual(d1,d2)

    def test_DistanceToLocation(self):
        """Distance from point1 to point2 same in other direction too"""
        point1 = (0.0, 0.0)
        point2 = (0.0, 1.0)
        d1 = distance(point1,point2)
        b1 = bearing(point1, point2)
        pointX = location(point1, d1, b1)
        print point2, pointX
        pointX = list(pointX)
        pointX[0] = round(pointX[0], 2)
        pointX[1] = round(pointX[1], 2)
        
        print point2, pointX
        
        self.assertEqual(list(point2), pointX)

if __name__ == '__main__':
    unittest.main()


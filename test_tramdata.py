import unittest
from tramdata import *

TRAM_FILE = './tramnetwork.json'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            self.tramdict = json.loads(trams.read())
            self.stopdict = self.tramdict['stops']
            self.linedict = self.tramdict['lines']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    def test_query_via(self):
        ans = answer_query(self.tramdict, "via Chalmers")
        self.assertEqual(ans, ['6', '7', '8', '10', '13'])

    def test_query_between(self):
        ans = answer_query(self.tramdict, "between Medicinaregatan and Saltholmen")
        self.assertEqual(ans, ['13'])

    def test_query_time_between(self):
        ans = answer_query(self.tramdict, "time with 5 from Munkebäckstorget to Sankt Sigfrids Plan")
        self.assertEqual(ans, 9)

    def test_query_distance_between(self):
        ans = answer_query(self.tramdict, "distance from Temperaturgatan to Lackarebäck")
        self.assertEqual(ans, 10.092)

    def test_query_unknown_arguments(self):
        ans = answer_query(self.tramdict, "between Medicinareberget and Saltholmen")
        self.assertEqual(ans, "unknown arguments")
        
    def test_query_try_again(self):
        ans = answer_query(self.tramdict, "distance between Chalmers and Ramberget")
        self.assertEqual(ans, "sorry, try again")
        
    def test_query_quit(self):
        ans = answer_query(self.tramdict, "quit")
        self.assertEqual(ans, None)

    def test_all_lines_exist(self):
        lines = []
        with open(LINE_FILE, "r", encoding="utf-8") as file: 
            for row in file: 
                if row.strip().endswith(":"):
                    line_number = row.strip().replace(":", "")
                    lines.append(line_number)
        
        for line in lines:
            self.assertIn(line, self.linedict, msg= line + " not in linedict")

    def test_all_stops_equal(self):
        with open(LINE_FILE, "r", encoding="utf-8") as file: 
            stops = None
            for row in file:
                if row.strip() == "":
                    continue
                else:
                    if row.strip().endswith(":"):
                        if stops != None:
                            self.assertListEqual(stops, self.linedict[line_number], msg= "stops are not equal for line " + line_number)
                        stops = []
                        line_number = row.strip().replace(":", "")
                    else:
                        stop = row[0:26].strip()
                        stops.append(stop)
            self.assertListEqual(stops, self.linedict[line_number], msg= "stops are not equal for line " + line_number)
                        
    def test_distances(self):
        for stop1 in self.stopdict.keys():
            for stop2 in self.stopdict.keys():
                self.assertLess(distance_between_stops(self.stopdict, stop1, stop2), 20, msg="unreasonable distance between stops " + stop1 + " and " + stop2)
    
    def test_pre_curr(self):
        for line, stops in self.linedict.items(): #values = stops 
            for stop1 in stops: 
                for stop2 in stops: 
                    self.assertEqual(time_between_stops(self.linedict, self.tramdict["times"], line, stop1, stop2), time_between_stops(self.linedict, self.tramdict["times"], line, stop2, stop1), msg = "The distance between stops is not equal both ways")
                         
        
    # add your own tests here
    # 

if __name__ == '__main__':
    unittest.main()


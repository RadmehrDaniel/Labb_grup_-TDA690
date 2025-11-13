import sys
import json
from haversine import haversine



# files given
STOP_FILE = './data/tramstops.json'
LINE_FILE = './data/tramlines.txt'
 
# file to give
TRAM_FILE = './tramnetwork.json'


def build_tram_stops(jsonobject):
    data = json.load(jsonobject)
    stops = {}
    for stop, stopdata in data.items():
        stops[stop] = {
            "lat": float(stopdata["position"][0]),
            "lon": float(stopdata["position"][1])
        }
    return stops

    # for stop, value_1 in data.items():
    #     if stop not in stops:  # If the stop doesn't exist in dict, add it.
    #         stops[stop] = {}  # Creates a nested dictionary inside stops, using the variable stop as the key.
    #     for pos, i in value_1.items():  # .items  to get the key and its value from a dict.
    #         if pos != "town":
    #             # print(i[0]) # Isolate the log. and the lat.
    #             # print(i[1])
    #             # Store in the dict. , stop is a variable no quotes, "lat" and "lon" are fixed string keys inside the inner dictionary --> use quotes.
    #             stops[stop]["lat"] = i[0]
    #             stops[stop]["lon"] = i[1]


def build_tram_lines(lines):  # lines is the file name.
    tram_lines = {}
    tram_times = {}
    prev_stop = None
    for row in lines:
        if row.strip() == "":  # removes empty lines
            continue
        else:
            if row.strip().endswith(":"):
                line_number = row.strip().replace(":", "")
                if line_number not in tram_lines:
                    tram_lines[line_number] = []  # Creating an empty list inside the dictionary.
                    prev_stop = None
            else:
                curr_stop = row[0:26].strip()
                tram_lines[line_number].append(curr_stop)

                # Tram times:

                curr_time = int(row.strip().split(":")[1])

                if prev_stop != None:
                    time_diff = curr_time - prev_time
                    if curr_stop not in tram_times or prev_stop not in tram_times[curr_stop]:
                        if prev_stop not in tram_times:
                            tram_times[prev_stop] = {}
                        tram_times[prev_stop][curr_stop] = time_diff

                prev_time = curr_time
                prev_stop = curr_stop

    return tram_lines, tram_times


def build_tram_network(stopfile, linefile):
    tram_network = {} # vi tar bort den eftersom att det inte behös då den definferas  där nere istöllet
    
    with open(linefile, encoding="utf-8") as line:
        tram_data = build_tram_lines(line)  # Tuple för "build_tram_lines" har (tram_lines, tram_times) renad definerade, så "tramdata" har den info
        tram_network["lines"] = tram_data[0] # eftersom "tram_data håller bara tram_lines, tram_times så sägger vi 'tram_data[0]' för att efteson line är 0 i index" 
        tram_network["times"] = tram_data[1]
    with open(stopfile, encoding="utf-8") as stop:
        stop_data = build_tram_stops(stop)
        tram_network["stops"] = stop_data # vi skirver på detta sätt, då om vi ksriver som övre metoded slkriver vi om den gammla, på detta sätt "Appedar" vi stops in i " tram_network"
    with open("tramnetwork.json", "w", encoding="utf-8") as network_file:
        json.dump(tram_network, network_file)

    # tram_network = { # sammas sak som det ovan men detta är snyggare men arne gillar det andra
    #     "lines": tram_data[0],
    #     "times": tram_data[1],
    #     "stops": stop_data
    # }
    
    
def lines_via_stop(linedict, stop):
    l_v_s = []
    for line, stops in linedict.items():
        if stop in stops:
            l_v_s.append(line)
    l_v_s.sort(key=lambda line: int(line))
    return l_v_s
            

def lines_between_stops(linedict, stop1, stop2):
    l_b_s = []
    for line, stops in linedict.items():
        if stop1 in stops and stop2 in stops:
            l_b_s.append(line)
    l_b_s.sort(key=lambda line: int(line))
    return l_b_s


def time_between_stops(linedict, timedict, line, stop1, stop2):
    if line not in lines_between_stops(linedict, stop1, stop2):
        print(f"Line does not go between {stop1} and {stop2}")
        return
    if stop1 == stop2:
        return 0
    time = 0
    count = False # eftersom vi börjar inte räkna hållplatser som är ikte relavanta
    for stop in linedict[line]:
        if count:
            if prev_stop in timedict and stop in timedict[prev_stop]:
                time += timedict[prev_stop][stop]  # ger tiden från föra stop till nuvarande stop 
            else:
                time += timedict[stop][prev_stop]
        if stop == stop1 or stop == stop2:
            if count:
                break
            count = True
        
        prev_stop = stop
    return time

def distance_between_stops(stopdict, stop1, stop2):
   
    stop1_coords = (stopdict[stop1]["lat"], stopdict[stop1]["lon"])
    stop2_coords = (stopdict[stop2]["lat"], stopdict[stop2]["lon"])
    return round(haversine(stop1_coords, stop2_coords), 3)
    

distance_between_stops(build_tram_stops(open(STOP_FILE)), "Chalmers", "Svingeln")  


def answer_query(tramdict, query):
    if query.startswith("via "):
        stop_name = query[4:].strip() #ta bort "via"
        if stop_name not in tramdict["stops"]: #Kontrollera att det är en riktig hållplats. 
            return "unknown arguments"
        return lines_via_stop(tramdict["lines"], stop_name)
    if query.startswith("between "):
        stops = query[8:].split(" and ")
        stop1 = stops[0].strip()
        stop2 = stops[1].strip()
        if stop1 not in tramdict["stops"] or stop2 not in tramdict["stops"]:
            return "unknown arguments"
        return lines_between_stops(tramdict["lines"], stop1, stop2)
    if query.startswith("time with "):
        q1 = query[10:].split(" from ") # "line from stop1 to stop2" --> ["line", "stop1 to stop2"]
        q2 = q1[1].split(" to ") # "stop1 to stop2" -> ["stop1", "stop2"]
        line = q1[0].strip()
        stop1 = q2[0].strip() 
        stop2 = q2[1].strip() 
        if stop1 not in tramdict["stops"] or stop2 not in tramdict["stops"] or line not in tramdict["lines"]:
            return "unknown arguments"
        return time_between_stops(tramdict["lines"], tramdict["times"], line, stop1, stop2)
    if query.startswith("distance from "):
        stops = query[14:].split(" to ")
        stop1 = stops[0].strip()
        stop2 = stops[1].strip()
        if stop1 not in tramdict["stops"] or stop2 not in tramdict["stops"]:
            return "unknown arguments"
        return distance_between_stops(tramdict["stops"], stop1, stop2)
    if query == "quit":
        return None
    return "sorry, try again"


def dialogue(tramfile=TRAM_FILE):
    with open(tramfile, "r", encoding="utf-8") as file:
        tram_data = json.load(file)
    while True:
        query = input("> ")
        result = answer_query(tram_data, query)
        if result == None:
            break
        print(result)
    

if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network(STOP_FILE,LINE_FILE)
    else:
        dialogue()
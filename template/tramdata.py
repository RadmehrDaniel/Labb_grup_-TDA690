import sys
import json

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
            "lat": stopdata["position"][0],
            "lon": stopdata["position"][1]
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



with open(STOP_FILE) as f:
    build_tram_stops(f)


def build_tram_lines(lines):  # lines is the file name.
    tram_lines = {}
    tram_times = {}
    prev_stop = None
    for row in lines:
        # print(f.read())
        if row.strip() == "":  # removes empty lines
            continue
        else:
            if row.strip().endswith(":"):
                line_number = row.strip().replace(":", "")
                if line_number not in tram_lines:
                    # for row in f[0:26].strip():
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



with open(LINE_FILE) as f:
    build_tram_lines(f)


def build_tram_network(stopfile, linefile):
    tram_network = {} # vi tar bort den eftersom att det inte behös då den definferas  där nere istöllet
    
    with open(linefile) as line:
        tram_data = build_tram_lines(line)  # Tuple för "build_tram_lines" har (tram_lines, tram_times) renad definerade, så "tramdata" har den info
        tram_network["lines"] = tram_data[0] # eftersom "tram_data håller bara tram_lines, tram_times så sägger vi 'tram_data[0]' för att efteson line är 0 i index" 
        tram_network["times"] = tram_data[1]
    with open(stopfile) as stop:
        stop_data = build_tram_stops(stop)
        tram_network["stops"] = stop_data # vi skirver på detta sätt, då om vi ksriver som övre metoded slkriver vi om den gammla, på detta sätt "Appedar" vi stops in i " tram_network"
    with open("tramnetwork.json", "w") as network_file:
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
    l_v_s.sort()
    print(l_v_s)
    return l_v_s
            

def lines_between_stops(linedict, stop1, stop2):
    l_b_s = []
    for line, stops in linedict.items():
        if stop1 in stops and stop2 in stops:
            l_b_s.append(line)
    l_b_s.sort()
    print(l_b_s)
    return l_b_s


def time_between_stops(linedict, timedict, line, stop1, stop2):
    time = 0
    count = False # efsrsom vi börajr inte räkna holplatser som är ikte relavanta
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
    print(time)
    return time
time_between_stops(*build_tram_lines(open(LINE_FILE)), "6", "Chalmers", "Svingeln")  

def distance_between_stops(stopdict, stop1, stop2):
    ## YOUR CODE HERE
    pass


def answer_query(tramdict, query):
    ## YOUR CODE HERE
    pass


def dialogue(tramfile=TRAM_FILE):
    ## YOUR CODE HERE
    pass

build_tram_network(STOP_FILE, LINE_FILE)

# if __name__ == '__main__':
#     if sys.argv[1:] == ['init']:
#         build_tram_network(STOP_FILE,LINE_FILE)
#     else:
#         dialogue()

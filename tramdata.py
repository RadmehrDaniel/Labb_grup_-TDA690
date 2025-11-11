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
    for stop, value_1 in data.items():
        if stop not in stops: # If the stop doesn't exist in dict, add it. 
            stops[stop] = {} #Creates a nested dictionary inside stops, using the variable stop as the key.
        for pos, i in value_1.items():  # .items  to get the key and its value from a dict.
            if pos != "town":
                #print(i[0]) # Isolate the log. and the lat. 
                #print(i[1])
                stops[stop]["lat"] = i[0] # Store in the dict. , stop is a variable no quotes, "lat" and "lon" are fixed string keys inside the inner dictionary --> use quotes.
                stops[stop]["lon"] =i[1]
            
        print(stops)
  

with open(STOP_FILE) as f:
    build_tram_stops(f)

def build_tram_lines(lines): #lines is the file name.
    tram_lines = {}
    tram_times = {}
    prev_stop = None
    for row in lines:
        #print(f.read())
        if row.strip() == "": #removes empty lines
            continue 
        else:
            if row.strip().endswith(":"):
                line_number = row.strip().replace(":","")
                if line_number not in tram_lines:
                #for row in f[0:26].strip():
                    tram_lines[line_number] = [] #Creating an empty list inside the dictionary.
            else: 
                curr_stop = row[0:26].strip()
                tram_lines[line_number].append(curr_stop)
                
                #Tram times:
                
                curr_time = int(row.strip().split(":")[1]) 
                
                if prev_stop != None: 
                    time_diff = curr_time - prev_time 
                    if curr_stop not in tram_times or prev_stop not in tram_times[curr_stop]:
                        if prev_stop not in tram_lines: 
                            tram_times[prev_stop] = {} 
                    tram_times[prev_stop][curr_stop] = time_diff 

            
                
            
                prev_time = curr_time
                prev_stop = curr_stop


    #print(tram_lines)

    print(tram_times)
   
         


with open(LINE_FILE) as f:
    build_tram_lines(f)

    


def build_tram_network(stopfile, linefile):
    ## YOUR CODE HERE
    pass

def lines_via_stop(linedict, stop):
    ## YOUR CODE HERE
    pass

def lines_between_stops(linedict, stop1, stop2):
    ## YOUR CODE HERE
    pass

def time_between_stops(linedict, timedict, line, stop1, stop2):
    ## YOUR CODE HERE
    pass

def distance_between_stops(stopdict, stop1, stop2):
    ## YOUR CODE HERE
    pass

def answer_query(tramdict, query):
    ## YOUR CODE HERE
    pass

def dialogue(tramfile=TRAM_FILE):
    ## YOUR CODE HERE
    pass

# if __name__ == '__main__':
#     if sys.argv[1:] == ['init']:
#         build_tram_network(STOP_FILE,LINE_FILE)
#     else:
#         dialogue()
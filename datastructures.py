import csv
from collections import defaultdict
from pprint import pprint
import math

airport_headers = []
route_headers = []
airport_model = {'code': None, 'name': None, 'city': None, 'country': None, 'latitude': None, 'longitude': None, 'routes':[]}
vertices = defaultdict(str, airport_model)
# CODE;NAME;CITY;COUNTRY;LATITUDE;LONGITUDE
edges = []
queue = []
cost_table = {}


# AIRLINE_CODE;SOURCE_CODE;DESTINATION_CODE;DISTANCE;TIME
def init():
    with open('data/airports.txt', 'r', encoding='latin1') as f:
        airport_headers = [item.rstrip().lstrip() for item in f.readline().split(';')]

        f.seek(0)
        print(airport_headers)
        csv_reader = csv.reader(f, delimiter=';')

        for row in csv_reader:

            vertices.update({row[0]:{'code': row[0], 'name': row[1], 'city': row[2], 'country': row[3], 'latitude': row[4], 'longitude': row[5]}})


    with open('data/routes.txt', 'r', encoding='latin1') as f:
        route_headers = [item.rstrip().lstrip() for item in f.readline().split(';')]
        print(route_headers)
        f.seek(0)
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            # print(row)
            edges.append({'airline_code':row[0], 'source_code':row[1], 'destination_code': row[2], 'distance':row[3], 'time':row[4]})

    #pprint(vertices)

# not in use (yet)
def run():
    init()
    running = True
    while running:
        # get input - switch case - run function based on input (with parameters)
        pass

def breadth_first(origin, destination, visited=[], queue=[]):
    # get origin's neighbours and add them to the queue
    # print('queue', queue)
    visited.append(origin)
    if origin == destination:
        return visited
    for e in edges:
        # print(e)
        if e['source_code']==origin and e['destination_code'] not in visited:
            # print('found route from ', origin)
            queue.append(e['destination_code'])

    if len(queue)<1:
        return None

    next_vertex = queue[0]
    queue = queue[1:]
    return breadth_first(next_vertex, destination, visited, queue)

def depth_first(origin, destination, visited=[], queue=[]):
    visited.append(origin)
    if origin == destination:
        return visited
    for e in edges:
        if e['source_code']==origin and e['destination_code'] not in visited:
            # print('found route from ', origin)
            queue.append(e['destination_code'])

    if len(queue)<1:
        return None

    next_vertex = queue[len(queue)-1]
    queue = queue[:-1]
    return breadth_first(next_vertex, destination, visited, queue)


def djikstra(origin, destination, by_distance=True):
    cost_table.clear()
    for v in vertices.keys():
        # print(v)
        if v==origin:
            cost_table.update({v:{'visited': False, 'cost': 0, 'parent': v}})
        else:
            cost_table.update({v:{'visited': False, 'cost': math.inf, 'parent': None}})
    if by_distance:
        return djikstra_distance(origin, destination)
    else:
        return djikstra_time(origin, destination)

def djikstra_distance(origin, destination, visited=[], queue=[]):

    visited.append(origin)
    cost_table[origin]['visited']==True
    if origin == destination:
        print('found destination', cost_table)
        return backtrack_cost_table(origin, destination)
    for e in edges:
        if e['source_code']==origin:
            if e['destination_code'] not in visited:
                queue.append(e['destination_code'])

            if float(e['distance']) + cost_table[origin]['cost'] < cost_table[destination]['cost']:
                cost_table[destination]['cost'] = float(e['distance']) + cost_table[origin]['cost']
                cost_table[destination]['parent']= origin

    if len(queue)<1:
        print('end of queue', cost_table)
        return backtrack_cost_table(origin, destination)

    next_vertex = queue[len(queue)-1]
    queue = queue[:-1]
    return breadth_first(next_vertex, destination, visited, queue)


def backtrack_cost_table(origin, destination, path=None):
    # print('cost table', cost_table)
    # print(cost_table)
    path = []
    current = destination
    while current != destination:
        path.append(current)
        current = cost_table[current]['parent']

    return path.reverse()




# def euclid(origin, destination):
#     for e in edges:
#         if e['source_code'] == source and e['destination_code'] == destination:
#             return e['distance']

init()
print(djikstra('LED', 'SCO'))

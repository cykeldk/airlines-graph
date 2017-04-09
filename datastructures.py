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
    return depth_first(next_vertex, destination, visited, queue)


def djikstra(origin, destination, by_distance=True):
    cost_table.clear()
    for v in vertices.keys():
        if v==origin:
            cost_table.update({v:{'visited': False, 'cost': 0, 'parent': v}})
        else:
            cost_table.update({v:{'visited': False, 'cost': math.inf, 'parent': None}})
    if by_distance:
        print('finding shortest route between {0} and {1}'.format(origin, destination))
        return djikstra_distance(origin, destination)
    else:
        print('finding fastest route between {0} and {1}'.format(origin, destination))
        return djikstra_time(origin, destination)

def djikstra_distance(origin, destination, original=None, queue=[]):
    # print('queue', queue)
    cost_table[origin]['visited']=True
    if not original:
        original = origin
    # are we there yet?
    if origin == destination:
        print('found destination')
        return backtrack_cost_table(original, destination)
    # i want ice-cream!
    for e in edges:
        if e['source_code']==origin:
            if cost_table[e['destination_code']]['visited'] == False and e['destination_code'] not in queue:
                queue.append(e['destination_code'])
            # check if route to edges destination_code is cheaper, if it is, update cost in cost_table
            if float(e['distance']) + cost_table[origin]['cost'] < cost_table[e['destination_code']]['cost']:
                cost_table[e['destination_code']]['cost'] = float(e['distance']) + cost_table[origin]['cost']
                cost_table[e['destination_code']]['parent']= origin
    # we're lost!
    if len(queue)<1:
        print('end of queue')
        return None

    next_vertex = queue[0]
    queue = queue[1:]
    return djikstra_distance(next_vertex, destination, original, queue)

def djikstra_time(origin, destination, original=None, queue=[]):
    transit_time = 60
    cost_table[origin]['visited']=True
    if not original:
        original = origin

    if origin == destination:
        print('found destination')
        return backtrack_cost_table(original, destination)


    for e in edges:
        if e['source_code']==origin:
            if cost_table[e['destination_code']]['visited'] == False and e['destination_code'] not in queue:
                queue.append(e['destination_code'])

            if float(e['time']) + cost_table[origin]['cost'] + 1 < cost_table[e['destination_code']]['cost']:

                # print('found cheaper route from {0} to {1}'.format(e['source_code'], e['destination_code'], e['time']))
                cost_table[e['destination_code']]['cost'] = float(e['time']) + cost_table[origin]['cost'] + 1
                cost_table[e['destination_code']]['parent']= origin

    if len(queue)<1:
        print('end of queue')
        return None

    next_vertex = queue[0]
    queue = queue[1:]
    # print('recursive call', len(queue))
    return djikstra_time(next_vertex, destination, original, queue)


def backtrack_cost_table(origin, destination):
    # print('cost table')
    # pprint(cost_table)

    #
    print('running backtrack from:\n{0}\nto:\n{1}\n'.format(cost_table[destination], cost_table[origin]) )
    # for k, v in cost_table.items():
    #     if v['visited']==True:
    #         print('airport: {0} route: {1}'.format(k,v))

    path = []
    current = destination
    print('current',current)
    print('origin', origin)
    while current != origin:
        # print('adding {0} to the path'.format(current))
        path.append(current)
        current = cost_table[current]['parent']
    path.append(origin)
    print('the path: {0}'.format(path))
    path.reverse()
    return path




# def euclid(origin, destination):
#     for e in edges:
#         if e['source_code'] == source and e['destination_code'] == destination:
#             return e['distance']

init()
print(breadth_first('THU', 'LAX'))

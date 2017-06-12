import csv
from collections import defaultdict
from pprint import pprint
import math
import sys
from tqdm import tqdm
import time

sys.setrecursionlimit(5000)

airport_headers = []
route_headers = []
airport_model = {'code': None, 'name': None, 'city': None, 'country': None, 'latitude': None, 'longitude': None, 'routes':[]}
vertices = defaultdict(str, airport_model)
edges = []
queue = []
cost_table = {}
all_airlines = set()


def init():
    with open('data/airports.txt', 'r', encoding='latin1') as f:
        airport_headers = [item.rstrip().lstrip() for item in f.readline().split(';')]
        f.seek(0)
        # print(airport_headers)
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            vertices.update({row[0]:{'code': row[0], 'name': row[1], 'city': row[2], 'country': row[3], 'latitude': row[4], 'longitude': row[5]}})

    with open('data/routes.txt', 'r', encoding='latin1') as f:
        route_headers = [item.rstrip().lstrip() for item in f.readline().split(';')]
        # print(route_headers)
        f.seek(0)
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            edges.append({'airline_code':row[0], 'source_code':row[1], 'destination_code': row[2], 'distance':row[3], 'time':row[4]})

    for e in edges:
        all_airlines.add(e['airline_code'])

def single_airline(origin, destination, breadth=True, show_progress=False):
    airline_list = set()

    for e in edges:
        if e['source_code']==origin:
            airline_list.add(e['airline_code'])

    if show_progress:
        if breadth:
            for a in tqdm(airline_list):
                if breadth_first(origin, destination, a):
                    return True
        else:
            for a in tqdm(airline_list):
                if depth_first(origin, destination, a):
                    return True
    else:
        if breadth:
            for a in airline_list:
                if breadth_first(origin, destination, a):
                    return True
        else:
            for a in airline_list:
                if depth_first(origin, destination, a):
                    return True
    return False


def breadth_first(origin, destination, airline, visited=[], queue=[]):
    visited.append(origin)
    if origin == destination:
        return True
    for e in edges:
        if e['source_code']==origin and e['airline_code']==airline:
            if e['destination_code'] not in visited and e['destination_code'] not in queue:
                queue.append(e['destination_code'])

    if len(queue)<1:
        return False

    next_vertex = queue[0]
    queue = queue[1:]
    return breadth_first(next_vertex, destination, airline, visited, queue)

def depth_first(origin, destination, airline, visited=[], queue=[]):
    visited.append(origin)
    if origin == destination:
        return visited
    for e in edges:
        if e['source_code']==origin and e['airline_code'] == airline:
            if e['destination_code'] not in visited and e['destination_code'] not in queue:
                queue.append(e['destination_code'])

    if len(queue)<1:
        return None

    next_vertex = queue[len(queue)-1]
    queue = queue[:-1]
    return depth_first(next_vertex, destination, airline, visited, queue)


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
            # check if route to edges destination_code is cheaper, if it is, update cost in cost_table
            if float(e['distance']) + cost_table[origin]['cost'] < cost_table[e['destination_code']]['cost']:
                cost_table[e['destination_code']]['cost'] = float(e['distance']) + cost_table[origin]['cost']
                cost_table[e['destination_code']]['parent']= origin
    if len(queue)<1:
        print('end of queue, the airport was not connected')
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
            # check if current route is cheaper than the one in cost_table
            if float(e['time']) + cost_table[origin]['cost'] + 1 < cost_table[e['destination_code']]['cost']:
                cost_table[e['destination_code']]['cost'] = float(e['time']) + cost_table[origin]['cost'] + 1
                cost_table[e['destination_code']]['parent']= origin

    if len(queue)<1:
        print('end of queue')
        return None

    next_vertex = queue[0]
    queue = queue[1:]
    return djikstra_time(next_vertex, destination, original, queue)


def backtrack_cost_table(origin, destination):
    print('backtracking from:\n{0}\nto:\n{1}\n'.format(cost_table[destination], cost_table[origin]) )
    path = []
    current = destination
    print('current',current)
    print('origin', origin)
    while current != origin:
        path.append(current)
        current = cost_table[current]['parent']
    path.append(origin)
    path.reverse()
    return path

def find_widest_coverage():
    airline_nodes = {}
    tmp_airports = None
    tmp_airline = None
    tmp_max_coverage = 0
    for a in tqdm(all_airlines):
        airports_covered, _ = run_prims_on_airline(a)
        if len(airports_covered) > tmp_max_coverage:
            tmp_max_coverage = len(airports_covered)
            tmp_airports = airports_covered
            tmp_airline = a

    print('there are {0} different airlines'.format(len(airline_nodes.keys())))
    return tmp_airline, tmp_max_coverage

def run_prims_on_airline(airline):
    # setting the stage
    a_visited = []
    a_edges = [i for i in edges if i['airline_code']==airline]
    a_vertices = []
    a_spanning_tree = []
    for e in a_edges:
        if e['destination_code'] not in a_vertices:
            a_vertices.append(e['destination_code'])
        if e['source_code'] not in a_vertices:
            a_vertices.append(e['source_code'])
    # doing the thing
    start = a_vertices[0]
    a_visited.append(start)
    action = True
    itercounter = 0
    while action:

        # print(itercounter)
        tmp_path = {'distance': -1}

        for path in a_edges:
            if path['source_code'] in a_visited and path['destination_code'] not in a_visited:
                itercounter += 1
                # print(itercounter, ' ', path)
                if float(path['distance']) > float(tmp_path['distance']):
                    tmp_path = path
        # print('temp path', tmp_path)
        if float(tmp_path['distance'])>-1 and tmp_path not in a_spanning_tree:
            a_spanning_tree.append(tmp_path)
            a_visited.append(tmp_path['destination_code'])
            a_edges.remove(path)
        else:
            return a_visited, a_spanning_tree


    print('{0} covers {1} routes between {2} airports'.format(airline, len(a_edges), len(a_vertices)))


def compareBfsAndDfs(times):
    acc_bfs_time = 0
    acc_dfs_time = 0
    winner = ''
    loser = ''
    difference = 0
    for i in range(times):
        #  breath first
        start_bfs = time.time()
        single_airline(fra, til, True)
        end_bfs = time.time()
        acc_bfs_time += end_bfs - start_bfs
        # depth first
        start_dfs = time.time()
        single_airline(fra, til, False)
        end_dfs = time.time()
        acc_dfs_time += end_dfs - start_dfs
    if acc_bfs_time < acc_dfs_time:
        winner = 'breath first'
        loser = 'depth first'
        difference = (acc_dfs_time - acc_bfs_time) / times
    else:
        winner = 'depth first'
        loser = 'breadth first'
        difference = (acc_bfs_time - acc_dfs_time) / times
    return winner, loser, difference


init()



fra = 'CPH'
til = 'HNL'
flyselskab = 'AA'
iterations = 10

# win, lose, average = compareBfsAndDfs(iterations)

# print('{0} is in average {2} faster than {1}'.format(win, lose, average))

winner, size = find_widest_coverage()
print('{0} has the widest coverage by {1} airports'.format(winner, size))
# print('it is {0} that i can get from {1} to {2} using a single airline'.format(single_airline(fra, til, False), fra, til))
# print('the shortest route between {0} and {1} is: {2}'.format(fra, til, djikstra(fra, til)))
# print('the fastest route between {0} and {1} is: {2}'.format(fra, til, djikstra(fra, til, False)))

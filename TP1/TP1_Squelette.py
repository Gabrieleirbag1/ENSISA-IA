import tkinter as tk
from tkinter import ttk
import csv
import random
from queue import Queue
from queue import LifoQueue
from queue import PriorityQueue
import math
import time
import os
import sys

search_algorithms = ('Parcours en largeur', 'Parcours en profondeur', 'Parcours en profondeur itératif', 'Recherche à coût Uniforme', 'Recherche gloutonne', 'A*')
costs = ('distance', 'temps')

town_color = 'lightcoral'
road_color = 'lightgreen'
path_color = 'red'

class Town:

    def __init__(self, dept_id, name, latitude, longitude):
        self.dept_id = dept_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.neighbours = dict()


class Road:

    def __init__(self, town1, town2, distance, time):
        self.town1 = town1
        self.town2 = town2
        self.distance = distance
        self.time = time

class Node:

    def __init__(self, town: Town, state: str, cost: int, parent, road_to_parent: Road, neighbours: list[Town]):
        self.town = town
        self.state = state
        self.cost = cost
        self.parent = parent
        self.road_to_parent = road_to_parent
        self.neighbours = neighbours

def get_neighbour_distance(town1_id, neighbour_town_id):
    for road in roads:
        if road.town1.dept_id == town1_id and road.town2.dept_id == neighbour_town_id:
            return road.distance
        elif road.town2.dept_id == town1_id and road.town1.dept_id == neighbour_town_id:
            return road.distance
    return None

def get_road_to_parent(parent_town: Town, child_town: Town) -> Road:
    for road in roads:
        if (road.town1 == parent_town and road.town2 == child_town) or (road.town2 == parent_town and road.town1 == child_town):
            return road
    return None

# Distance vol d'oiseau
def crowfliesdistance(town1, town2):
    
    return 0

# A-Star
def a_star(start_town, end_town):
    # À remplir !
    return None

# Recherche gloutonne
def greedy_search(start_town, end_town):
    # À remplir !
    return None

# Parcours à coût uniforme
def ucs(start_town, end_town):
    # À remplir !
    return None

# Parcours en profondeur itératif
def dfs_iter(start_town, end_town, max_depth=0):
    # si max_depth est == 0 alors il n'y a pas de limite à la recherche
    depth = 0
    while depth <= max_depth or max_depth == 0:
        to_visit_queue = LifoQueue()
        visited = set()
        node = Node(start_town, "explored", 0, None, None, start_town.neighbours)
        to_visit_queue.put((node, 0))
        
        while not to_visit_queue.empty():
            node, current_depth = to_visit_queue.get()
            
            if node.town in visited:
                continue
            visited.add(node.town)
            
            print(f"Visiting town {node.town.dept_id} at depth {current_depth}")

            if node.town == end_town:
                print("Found it!")
                return node
            
            if current_depth < depth:
                for neighbour_town in node.town.neighbours.keys():
                    if neighbour_town in visited:
                        continue
                    
                    parent = node
                    road_to_parent = get_road_to_parent(parent.town, neighbour_town)

                    neighbour_node = Node(
                        neighbour_town, 
                        "frontier",
                        0,
                        parent,
                        road_to_parent,
                        neighbour_town.neighbours
                    )

                    to_visit_queue.put((neighbour_node, current_depth + 1))
        
        depth += 1
        if max_depth > 0 and depth > max_depth: 
            # arreter le code si on a mis une limite de recherche maximale
            break
    
    return None


# Parcours en profondeur
def dfs(start_town, end_town):
    # À remplir !
    to_visit_queue = LifoQueue()
    visited = set()
    node = Node(start_town, "explored", "", None, None, start_town.neighbours)
    to_visit_queue.put(node)
    while not to_visit_queue.empty():
        node = to_visit_queue.get()
        
        if node.town in visited:
            continue
        visited.add(node.town)
        
        # print("Visiting town ", node.town.dept_id)

        if node.town == end_town:
            print("Found it!")
            return node
        for neighbour_town in node.town.neighbours.keys():

            if neighbour_town in visited:
                continue
            distance = 0
            parent = node
            road_to_parent = get_road_to_parent(parent.town, neighbour_town)

            neighbour_node = Node(
                neighbour_town, 
                "frontier",
                distance,
                parent,
                road_to_parent,
                neighbour_town.neighbours
            )

            to_visit_queue.put(neighbour_node)

    return None

# Parcours en largeur
def bfs(start_town: Town, end_town: Town):
    # À remplir !
    to_visit_queue = Queue()
    visited = set()
    node = Node(start_town, "explored", "", None, None, start_town.neighbours)
    to_visit_queue.put(node)
    while not to_visit_queue.empty():
        print("Visiting town ", node.town.dept_id)
        for neighbour_town in node.town.neighbours.keys():
            if neighbour_town in visited:
                continue
            visited.add(neighbour_town)

            # distance = get_neighbour_distance(start_town.dept_id, neighbour_town.dept_id)
            distance = 0

            parent = node

            road_to_parent = get_road_to_parent(parent.town, neighbour_town)

            neighbour_node = Node(
                neighbour_town, 
                "frontier",
                distance,
                parent,
                road_to_parent,
                neighbour_town.neighbours
            )

            to_visit_queue.put(neighbour_node)

            # print(distance, start_town.dept_id, neighbour_town.dept_id)
            if neighbour_town == end_town:
                print("Found it!")
                return neighbour_node
        node = to_visit_queue.get()
    return None

def display_path(path):
    current_node = path
    while current_node.parent is not None:
        canvas1.itemconfig(road_lines[current_node.road_to_parent], fill=path_color)
        # print(current_node.road_to_parent.town1.name, current_node.road_to_parent.town2.name)
        current_node = current_node.parent


def run_search():
    button_run['state'] = tk.DISABLED
    # put all the roads in normal
    for road in roads:
        canvas1.itemconfig(road_lines[road], fill=road_color)
    start_city = towns[combobox_start.current() + 1]
    end_city = towns[combobox_end.current() + 1]
    search_method = combobox_algorithm.current()
    cost = combobox_cost.current()
    computing_time = time.time()
    if search_method == 0:  # Parcours en largeur
        path = bfs(start_city, end_city)
    elif search_method == 1:  # Parcours en profondeur
        path = dfs(start_city, end_city)
    elif search_method == 2:  # Parcours en profondeur itératif
        path = dfs_iter(start_city, end_city)
    elif search_method == 3:  # Parcours à coût uniforme
        path = ucs(start_city, end_city)
    elif search_method == 4:  # Recherche gloutonne
        path = greedy_search(start_city, end_city)
    elif search_method == 5:  # A*
        path = a_star(start_city, end_city)
    else:
        path = None
    computing_time = time.time() - computing_time
    if path is not None:
        label_path_title['text'] = "Itinéraire de "+start_city.name+" à "+end_city.name+" avec "+search_algorithms[search_method]
        label_distance['text'] = "Distance: "+str(path.cost)+"km"
        label_computing_time['text'] = "Temps de calcul: "+str(computing_time)+"s"
        display_path(path)
    button_run['state'] = tk.NORMAL


def longitude_to_pixel(longitude):
    return (longitude-map_W) * diff_W_E

def latitude_to_pixel(latitude):
    return (map_N - latitude) * diff_N_S


# Read towns and roads csv and create relative objects
towns = dict()
roads = list()
with open(os.path.join(os.path.dirname(__file__), 'data', 'towns.csv'), newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for road in reader:
        towns[int(road['dept_id'])] = Town(dept_id=int(road['dept_id']), name=road['name'], latitude=float(road['latitude']), longitude=float(road['longitude']))
with open(os.path.join(os.path.dirname(__file__), 'data', 'roads.csv'), newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for road in reader:
        road = Road(town1=towns[int(road['town1'])], town2=towns[int(road['town2'])], distance=int(road['distance']), time=int(road['time']))
        roads.append(road)
        road.town1.neighbours[road.town2] = road
        road.town2.neighbours[road.town1] = road


window = tk.Tk()
window.title("Itineria")

# Décommenter la carte pour choisir la bonne taille pour votre machine
# map_image = tk.PhotoImage(file="img/France_map_admin_1066_1024.png")
map_image = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "img/France_map_admin_799_768.png"))
# map_image = tk.PhotoImage(file="img/France_map_admin_499_480.png")



width = map_image.width()
height = map_image.height()
canvas1 = tk.Canvas(window, width=width, height=height)

background_map = canvas1.create_image(0, 0, anchor=tk.NW, image=map_image)

# Dessin des routes et villes
map_N = 51.5
map_S = 41
map_W = -5.8
map_E = 10
diff_W_E = width / (map_E - map_W)
diff_N_S = height / (map_N - map_S)
town_radius = 4
road_width = 3

road_lines = dict()
for road in roads:
    road_lines[road] = canvas1.create_line(longitude_to_pixel(road.town1.longitude), latitude_to_pixel(road.town1.latitude),
                        longitude_to_pixel(road.town2.longitude), latitude_to_pixel(road.town2.latitude), fill=road_color,
                        width=road_width)

for town in towns.values():
    canvas1.create_oval(longitude_to_pixel(town.longitude) - town_radius, latitude_to_pixel(town.latitude) - town_radius,
                        longitude_to_pixel(town.longitude) + town_radius, latitude_to_pixel(town.latitude) + town_radius,
                        fill=town_color)


canvas1.grid(row=0, column=0, columnspan=4)
label_start = tk.Label(window, text="Départ")
label_start.grid(row=1, column=0)
combobox_start = ttk.Combobox(window, state='readonly')
combobox_start.grid(row=1, column=1)

label_end = tk.Label(window, text="Arrivée")
label_end.grid(row=1, column=2)
combobox_end = ttk.Combobox(window, state='readonly')
combobox_end.grid(row=1, column=3)

town_list = []
for town in towns.values():
    town_list.append(str(town.dept_id)+" - "+town.name)
combobox_start['values'] = town_list
combobox_end['values'] = town_list
combobox_start.current(random.randint(0, len(town_list)-1))
combobox_end.current(random.randint(0, len(town_list)-1))

label_algorithm = tk.Label(window, text="Algorithme")
label_algorithm.grid(row=2, column=0)
combobox_algorithm = ttk.Combobox(window, state='readonly')
combobox_algorithm.grid(row=2, column=1)
combobox_algorithm['values'] = search_algorithms
combobox_algorithm.current(random.randint(0, len(combobox_algorithm['values'])-1))

label_cost = tk.Label(window, text="Coût")
label_cost.grid(row=2, column=2)
combobox_cost = ttk.Combobox(window, state='readonly')
combobox_cost.grid(row=2, column=3)
combobox_cost['values'] = costs
combobox_cost.current(random.randint(0, len(combobox_cost['values']) - 1))

label_path_title = tk.Label(window, text="")
label_path_title.grid(row=3, column=0, columnspan=4)

label_distance = tk.Label(window, text="")
label_distance.grid(row=4, column=0)

label_computing_time = tk.Label(window, text="")
label_computing_time.grid(row=4, column=3)

button_run = tk.Button(window, text='Calculer', command=run_search)
button_run.grid(row=5, column=0)

button_quit = tk.Button(window, text='Quitter', command=window.destroy)
button_quit.grid(row=5, column=3)
window.mainloop()

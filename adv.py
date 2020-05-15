from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

def add_room_to_graph(room, neighbors):
# def add_room_to_graph(room):
    # traversal_graph[room] = {'n': '?', 's': '?', 'e': '?', 'w': '?'}
    # print(neighbors)
    # traversal_graph[room] = {neighbors[i]: '?' for i in range(0, len(neighbors))}
    traversal_graph[room] = neighbors

def add_exits_to_room(dirs):
    exits = {}
    for exit in dirs:
        next_room = player.current_room.get_room_in_direction(exit).id
        exits[exit] = next_room
    
    return exits

traversal_path = []
traversal_graph = {}
visited = [None]

# add start room to graph
add_room_to_graph(player.current_room.id, add_exits_to_room(player.current_room.get_exits()))

q = Queue()
q.enqueue(player.current_room.id)

s = Stack()
s.push(player.current_room.id)
# s = []
# s.append(player.current_room.id)

visited = set()

while q.size() > 0:

    current_room = q.dequeue()
    
    if current_room not in traversal_graph:
        # Get current_room exits
        room_exits = player.current_room.get_exits()
        # Add current_room with neighbors to traversal_graph
        add_room_to_graph(current_room, add_exits_to_room(room_exits))

    else:
        print(f'Room {current_room} visited')

    for k, v in traversal_graph[current_room].items():
        print(k, v)


# print(traversal_graph)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

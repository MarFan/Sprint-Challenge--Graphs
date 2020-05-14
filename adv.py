from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

def add_room_to_graph(room, dirs):
    travel_graph[room] = dirs

def make_exits(dirs):
    exits = {}
    for exit in dirs:
        next_room = player.current_room.get_room_in_direction(exit).id
        exits[exit] = next_room
    
    return exits

traversal_path = []
travel_graph = {}

start_room = player.current_room.id

# add start room to graph
add_room_to_graph(start_room, make_exits(player.current_room.get_exits()))

q = []
q.append(start_room)

while len(q):
    current_room = q.pop()

    # if the current room is not in the graph, add it
    if current_room not in travel_graph:
        room_exits = player.current_room.get_exits()
        # add current_room to graph
        add_room_to_graph(current_room, make_exits(room_exits))
    
    # move to next room
    for key in travel_graph[current_room]:
        traversal_path.append(key)
 
# print(q)

# while len(q):
#     r = q.pop()


#     if current_room.id not in travel_graph:
#         travel_graph[player.current_room.id] = {}
#     # print(current_room.id)
    
#     for exit in current_room.get_exits():
#         next_room = current_room.get_room_in_direction(exit).id
#         if exit not in travel_graph[current_room.id]:
#             travel_graph[current_room.id][exit] = next_room
    
#     #     q.append(next_room)

print(travel_graph)

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

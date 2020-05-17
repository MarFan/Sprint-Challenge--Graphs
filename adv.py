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

def add_room_to_graph(room, exits):
    traversal_graph[room] = {}
    for exit in exits:
        traversal_graph[room][exit] = '?'

# Conversion for the room you came from
reverse_direction = {'n': 's', 'w': 'e', 's': 'n', 'e': 'w'}

# The path to follow
traversal_path = []

traversal_graph= {}

# Starting room
starting_room = player.current_room.id
starting_room_exits = player.current_room.get_exits()

# Add first room to traversal_graph
# add_room_to_graph(starting_room, starting_room_exits)

prev_room = None

# picks a random unexplored direction to start
# travel_dir = random.choice(starting_room_exits)
travel_dir = None

s = Stack()
# Add the id of the starting room
s.push(starting_room)

q = Queue()
visited = set()

while len(traversal_graph) < len(room_graph):

    # follows n until it can't go any farther and waits...
    while s.size():
        
        current_room = s.pop()

        if current_room not in traversal_graph:
            room_exits = player.current_room.get_exits()
            add_room_to_graph(current_room, room_exits)

            # print(prev_room, traversal_graph[current_room].items())
            # print(f'Room {current_room} added', prev_room, current_room)

        if prev_room is not None:
            traversal_graph[prev_room][travel_dir] = current_room
            traversal_graph[current_room][reverse_direction[travel_dir]] = prev_room
        # print(traversal_path)

        # print(travel_dir, current_room)
        # This always goes north 
        # turn in to random direction ??
        for room_dir, room_id in traversal_graph[current_room].items():
            # find the first unvisited room and head that way
            # tends to be north
            if room_id == '?':
                # print(room_dir)
                travel_dir = room_dir
                prev_room = current_room
                player.travel(travel_dir)
                traversal_path.append(travel_dir)
                s.push(player.current_room.id)
                # print('Move',room_dir, room_id, prev_room, player.current_room.id)
                break
            else:
                # print('Chill',room_dir, room_id, prev_room, player.current_room.id)
                # print(traversal_graph)
                s.pop()
        # print(current_room)
        # print(traversal_graph)

    # Stuck at a dead end, go back one step
    # if len(player.current_room.get_exits()) == 1:
    #     # print('Waiting', player.current_room.id)
    #     # print(traversal_path)
    #     travel_dir = reverse_direction[travel_dir]
    #     player.travel(travel_dir)
    #     traversal_path.append(travel_dir)
    #     # print(traversal_path, player.current_room.id)
    #     s.push(player.current_room.id)
        


    # create an empty queue

    # queue up current room

    # Path = []
    #     if room has unvisited neighbors
    #         break

    #     add rooms that neighbors have been visited


    # travers the path back to a room
    #     maybe reverse the list

    # queue up current room player is waiting in
    
    q.enqueue([player.current_room.id])

    while q.size():
        path = q.dequeue()
        current_room = path[-1]
        
        if current_room not in visited:
            visited.add(current_room)
            # print(current_room, traversal_graph[current_room].values())
            if '?' in traversal_graph[current_room].values():
                print('Going back', path)
                for room_dir, room_id in traversal_graph[current_room].items():
                    pass
                    # print(prev_room, current_room, room_dir, room_id)
                    # if room_id == prev_room:
                    #     # print(current_room, reverse_direction[room_dir])
                    #     player.travel(reverse_direction[room_dir])
                    #     traversal_path.append(reverse_direction[room_dir])
                    #     s.push(current_room)
                
            else:
                print('Going back', path)
                for room_dir, room_id in traversal_graph[current_room].items():
                    # if room_id != '?':
                    # traversal_graph[current_room]
                    prev_room = current_room
                    new_path = list(path)
                    new_path.append(room_id)
                    # traversal_path.append(room_dir)
                    # player.travel(room_dir)
                    # print(path, new_path)
                    q.enqueue(new_path)
            # print(player.current_room.id)
        # print(player.current_room.id)
    # print(q.size())
    # print(new_path)

        # print(path)
    # print(traversal_path)        







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

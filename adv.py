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

while len(traversal_graph) < len(room_graph):

    while s.size() > 0:
        current_room = s.pop()

        if current_room not in traversal_graph:
            room_exits = player.current_room.get_exits()
            add_room_to_graph(current_room, room_exits)

        if prev_room is not None:
            traversal_graph[prev_room][travel_dir] = current_room
            traversal_graph[current_room][reverse_direction[travel_dir]] = prev_room

        if '?' in traversal_graph[current_room].values():
            room_exits = []
            for room_dir, room_id in traversal_graph[current_room].items():
                if room_id == '?':
                    room_exits.append(room_dir)

            travel_dir = random.choice(room_exits)
            # print(f'{player.current_room.id}, {current_room} heading {travel_dir}')
            prev_room = current_room
            player.travel(travel_dir)
            traversal_path.append(travel_dir)
            s.push(player.current_room.id)
        else:
            s.pop()
            # q.enqueue([current_room])

        # print(traversal_path, player.current_room.id, current_room)
    
    q.enqueue([player.current_room.id])
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        current_room = path[-1]
        # print('queue', traversal_path, player.current_room.id, current_room)
        if current_room not in visited:
            visited.add(current_room)
            if '?' in traversal_graph[current_room].values():
                break
            else:
                for next_room in traversal_graph[current_room].values():
                    prev_room = current_room
                    new_path = list(path)
                    new_path.append(next_room)
                    q.enqueue(new_path)

    
    while len(path) > 0:
        next_room = path.pop(0)
        if next_room is not player.current_room.id:
            # print(player.current_room.id, next_room, path)
            for room_dir, room_id in traversal_graph[player.current_room.id].items():
                if traversal_graph[player.current_room.id][room_dir] == next_room:
                    # move the player
                    player.travel(room_dir)
                    # append it to traversal_path
                    traversal_path.append(room_dir)
                    print(player.current_room.id, traversal_path)
        # else:
        #     path.pop()
                
    s.push(player.current_room.id)

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

# imports
from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def add_to_visited(room_id, visited):
    if room_id not in visited:
        visited[room_id] = {'n': '?', 's': '?', 'e': '?', 'w': '?'}
    return visited


def reverse_direction(direction):
    if direction == "n":
        return "s"
    if direction == "s":
        return "n"
    if direction == "e":
        return "w"
    if direction == "w":
        return "e"


def possible_exits(room_id, player, visited):
    choices = player.current_room.get_exits()
    possible_choices = []
    for direction, target_room_id in visited[room_id].items():
        if direction in choices and target_room_id == '?':
            possible_choices.append(direction)
    return possible_choices


def traverse_all_rooms(player):
    visited = {}
    visited_path = []
    queue = Queue()
    queue.enqueue(player.current_room.id)

    while queue.size() > 0:
        if len(visited) == len(world.rooms):
            return visited
        
        room_id = queue.dequeue()
        visited = add_to_visited(room_id, visited)
        
        
        if len(visited_path) > 0:
            prev_room_id = visited_path[-1][0]
            prev_room_dir = reverse_direction(visited_path[-1][1])
            visited[room_id][prev_room_dir] = prev_room_id
        
        choices = possible_exits(room_id, player, visited)
        
        if choices:
            choice = random.choice(choices)
            player.travel(choice)
            visited[room_id][choice] = player.current_room.id
            visited_path.append([room_id, choice])
            
        else:
            choice = prev_room_dir
            player.travel(choice)
            if visited_path:
                visited_path.pop()
            else:
                traversal_path.append(choice)
                return visited
        
        traversal_path.append(choice)
        queue.enqueue(player.current_room.id)
        print(visited_path)


player = Player(world.starting_room)
traverse_all_rooms(player)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
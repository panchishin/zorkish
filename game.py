import random
import json
from ollama import make_rooms

# Some fun flavour text to start off
character_descriptions = ["tall", "short", "sly", "lanky", "blue"]
character_gender = ["male","female"]
character_race = ["human","goblin"]

description = random.choice(character_descriptions) + " " + random.choice(character_gender) + " " + random.choice(character_race)

print()
print("You are a " + description + " exploring the dangerous underground")



# Define some synonyms for frequently used commands
synonyms = {"n":"north","s":"south","e":"east","w":"west","ne":"northeast","nw":"northwest","se":"southeast","sw":"southwest",
"u":"up","d":"down","p":"portal","i":"inventory","desc":"describe","look":"describe",
"quit":"exit","bye":"exit"} 



# Define the rooms in the underground
# a room has exits to other rooms and a description and items
rooms = json.load(open("rooms.json"))

# add a loot list to every room
for room in rooms:
    rooms[room]['loot'] = rooms[room].get('loot',list())

# loot to find that is scattered around the place
loot = json.load(open("loot.json"))

# assign loot to room
for item in loot:
    rooms[random.choice(loot[item]['possible_spawn_room'])]['loot'].append(item)

# The player data.  Not much yet, but we can add more
current_room = "Welcome"
players_loot = []


# Check if room has an undefined exit
def check_empty_exits(current_room):
    if "" in rooms[current_room]['exits'].values():
        return True

# Find rooms with undefined exits
def find_empty_exits():
    empty_exits = []
    for room in rooms:
        if check_empty_exits(room):
            empty_exits.append(room)
    return empty_exits

# Create a new room by calling ollama
def create_room(current_room):
    # TODO call make_rooms
    pass

# Print the description and contents of a room
def printroom(current_room):
    print()
    print("Location : " + current_room)
    print(rooms[current_room]['description'])
    print("There are exits : " + ", ".join(rooms[current_room]['exits']))
    if 'loot' in rooms[current_room] and len(rooms[current_room]['loot']) > 0:
        print("You see the following : " + ", ".join(rooms[current_room]['loot']))


# Main Game Loop
action = "describe"
while action != "exit":

    if action in synonyms:
        action = synonyms[action]

    # go in a direction if possible
    if action in rooms[current_room]['exits']:
        current_room = rooms[current_room]['exits'][action]
        printroom(current_room)

    # describe the room
    elif action == "describe":
        printroom(current_room)

    # helpful message if trying to go in an invalid direction
    elif action in ['north','south','east','west','northeast','northwest','southeast','southwest','up','down','portal']:
        print("It doesn't appear there is an exit in that direction")
        printroom(current_room)

    # take loot
    elif 'loot' in rooms[current_room] and action in rooms[current_room]['loot']:
        print("You take the " + action)
        print("Description : " + loot[action]['description'])
        rooms[current_room]['loot'] = [x for x in rooms[current_room]['loot'] if x != action]
        players_loot.append(action)

    # check inventory
    elif action == "inventory":
        print("you are carrying : ", end="")
        if len(players_loot) == 0:
            print("nothing")
        else :
            print(", ".join(players_loot))

    # drop loot
    elif action in players_loot:
        print("You drop the " + action)
        if 'look' not in rooms[current_room]:
            rooms[current_room]['loot'] = []
        rooms[current_room]['loot'].append(action)
        players_loot.remove(action)

    # Don't understand player
    else :
        print("I don't understand.  Try saying an exit, an item name, inventory, or describe.")

    print("")    
    action = input("What do you do? ")


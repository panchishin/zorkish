import random


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
rooms = {}

rooms["Welcome"] = { 
    'exits' : { 'start': 'Entrance', 'exit': 'Welcome' } , 
    'description' : """Welcome to the fabulous underground.
You will be provided with danger, exploration, loot, and certain death.
Explore directions by saying that direction.  Exit this room by typing
the name of the exit listed below.

Other commands you can use are 'inventory' and 'describe'.
To pick up an item type the name of it."""}

rooms["Entrance"] = { 
    'exits' : { 'north': 'Dark Hallway' } , 
    'description' : 'You are at the entrance of the dungeon'}

rooms["Dark Hallway"] = { 
    'exits' : { 'south':'Entrance', 'northwest': 'Abyss Top' } , 
    'description' : 'This hallway is dark'}

rooms["Abyss Top"] = { 
    'exits' : { 'southeast':'Dark Hallway', 'down':'Deep Abyss' } , 
    'description' : 'Your soul feels heavy and in this place you feel no hope'}

rooms["Deep Abyss"] = {
    'exits' : { 'up':'Abyss Top', 'east':'Eastern Narrow Tunnel', 'west':'Western Narrow Tunnel', 'portal':'Purple plains'},
    'description' : """Your will feels broken and your heart beats pale limp thumps.
This place is near an evil beyond anything you've experience before.
Fleeing back up is possible.  Narrow tunnels span east and west.
Surrounded in cobble stone and adorned with skulls stands a single glowing portal in this vast pit."""}

rooms["Eastern Narrow Tunnel"] = {
    'exits' : {"west":"Deep Abyss"},
    'description' : "This is a dead End"}

rooms["Western Narrow Tunnel"] = {
    'exits' : {"east":"Deep Abyss"},
    'description' : "This is a dead End"}

rooms["Purple plains"] = {
    'exits' : {"portal":"Deep Abyss"},
    'description' : """An infinite expanse of purple flowers stretches out in all directions.
Fluffy clouds dot the sky, shielding you from a summer sun.  A cool breeze lifts
the fragrance from the fields and refreshes you.
An arch made of volcanic glass vibrates with wicked energy, providing a portal to horrors."""}

# add a loot list to every room
for room in rooms:
    rooms[room]['loot'] = rooms[room].get('loot',list())

# loot to find that is scattered around the place
loot = {}

loot['knife'] = { 
    'possible_spawn_room' : ['Entrance','Dark Hallway'], 
    'description' : 'A trusty blade with a business end you would rather not be on the receiving side of' , 
    'value' : 5 }

loot['skull'] = { 
    'possible_spawn_room' : ['Eastern Narrow Tunnel','Western Narrow Tunnel'], 
    'description' : 'It was a human, possibly ugly' , 
    'value' : -2 }

# assign loot to room
for item in loot:
    rooms[random.choice(loot[item]['possible_spawn_room'])]['loot'].append(item)

# The player data.  Not much yet, but we can add more
current_room = "Welcome"
players_loot = []


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


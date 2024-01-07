import json
import requests

url = "http://localhost:11434/api/chat"


def call(request_text, max_length=1000):
    to_mistral = {
      "model": "mistral",
      "messages": [ { "role": "user", "content": request_text } ]
    }

    # Send an HTTP request with the JSON data in the body and read response content in chunks
    response = requests.post(url, data=json.dumps(to_mistral).encode(), stream=True)

    result = []
    print(end="Thinking ")
    for chunk in response.iter_content(None, decode_unicode=True):
        if chunk:
            message = json.loads(chunk)
            content = message.get('message', {}).get('content')
            if content:
                result.append(content)
                if len(content) % 5 == 0:
                    print(end=".", flush=True)
            if len(content) > max_length:
                break
    print(" completed")
    result = "".join(result)
    return result

make_room_prompt = """We are making a dungeon exploration game together.  Inspired by Zork, the game is text based, has rooms with things and puzzles.  My following question will be around creating content for this game.  As context, here is a list of rooms we have created so far: ROOMS.  All content you create is expect to be JSON parsable.  Here is your next task:  create a list of three unique rooms.  Each room should have the following attributes defined: name, inventory (a list of items that the player can find, usually only 1 but sometimes more), deadend (true if it is a dead end), description (2 to 5 sentences describing the room).

Example start:
 {
 "rooms": [
  {
   "name":

Start:
"""

def make_rooms(room_name_list):
    response = call(make_room_prompt.replace("ROOMS",", ".join(room_name_list)))

    try:
        rooms = json.loads(response)
    except ValueError:
        try:
            rooms = json.loads('{ "rooms": [ {' + response)
        except ValueError:
            try:
                rooms = json.loads('{ "rooms": [' + response)
            except ValueError:
                rooms = {"rooms":[]}

    rooms["rooms"] = rooms.get("rooms", []) 
    rooms = rooms["rooms"]
    return rooms


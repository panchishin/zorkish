import json
import requests

def call(request_text, temperature=0.4):
    url = "http://localhost:11434/api/chat"

    to_mistral = {
      "model": "mistral:7b-instruct-q6_K",
      "messages": [ { "role": "user", "content": request_text }],
      "stream": False,
      "format": "json",
      "options": {"temperature": temperature},
    }

    # Send an HTTP request with the JSON data in the body and read response content in chunks
    response = requests.post(url, data=json.dumps(to_mistral).encode(), stream=False)

    # Just return the contens of the message
    return json.loads(response.content.decode())['message']['content']


make_room_prompt = """
We are collaborating on the creation of a text-based dungeon exploration game, reminiscent of Zork's intrigue and mystery. For our next stage in content development, I present you with this task: design three distinct rooms for our game.

As context, here a list of rooms we have established so far: ROOMS.

All content you generate must be JSON parsable. Here's your assignment: create a set of three unique rooms. Each room should possess the following attributes defined:

- name: (Choose a descriptive and distinctive title)
- description: (Compose 3 to 5 evocative sentences that bring the room to life)

Example start:
 {
 "rooms": [
  {
   "name": "The Whispering Chamber",
   "description": "A hush falls over you as you enter this chamber. The walls are adorned with ancient runes that seem to glow in the dim light, casting eerie shadows across the floor. A musty scent fills 
your nostrils, and a faint humming can be heard, like the sound of distant water. In the center of the room stands an ornate pedestal, upon which rests a mysterious crystal orb."
  }
 ]
}"""

def make_rooms(room_name_list):
    response = call(make_room_prompt.replace("ROOMS",", ".join(room_name_list)))

    # The response is text, but we want to return a JSON object
    response_json = json.loads(response)

    # From our prompt we expect all the data to be in the 'rooms' key
    return response_json.get("rooms", []) 


if __name__ == "__main__":
    a = make_rooms(["Grand Entrance to Palace", "Top of Spiral Stairs", "Powder Room on 2nd Floor", "The Enchanted Library", "The Crystal Cavern"])
    print(json.dumps(a, indent=2))
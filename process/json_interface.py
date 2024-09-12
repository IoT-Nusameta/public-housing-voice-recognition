import os
import json
from dotenv import load_dotenv

load_dotenv()
parent_path = os.getenv('PARENT_PATH')
relay_path = parent_path + '/temp/relay.json'

def load_json():
    with open(relay_path, 'r') as openfile:
        json_object = json.load(openfile)
        return json_object

def read_relay(relay):
    loaded_data = load_json()
    state = loaded_data[f'{relay}']
    return state

def make_state_relay(relay, state):
    loaded_data = load_json()
    loaded_data[f'{relay}'] = state

    with open(relay_path, 'w') as file:
        json.dump(loaded_data, file, indent=2)

# print(read_relay('relay2'))
# make_state_relay('relay3', True)
import utils
import json
from fastapi import FastAPI

app = FastAPI()

# Step 1: Read the JSON file
with open('Data/UserData.json', 'r') as file:
    data = json.load(file)

# Step 2: Modify the data
data['text'] = 'new_value'  # Update a key

# Step 3: Write the updated data back to the file
with open('Data/UserData.json', 'w') as file:
    json.dump(data, file, indent=4)  # Use indent for pretty formatting

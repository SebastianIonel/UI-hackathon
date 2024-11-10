import requests
import json


url = "http://192.168.0.131:5000/bulk"


def bulk():

    url = "http://192.168.0.131:5000/bulk"
    file_path = 'input.json'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Save the JSON response to a file
            with open(file_path, 'w') as file:
                json.dump(response.json(), file, indent=4)
            print("Response has been written to input.json")
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

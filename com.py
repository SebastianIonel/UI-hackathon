import requests
import json

def bulk():

    url = "http://192.168.0.131:5000/bulk"
    file_path = 'input.json'

    try:
        response = requests.get(url)
        with open(file_path, 'w') as file:
            json.dump(response.json(), file, indent=4)
        print("Response has been written to input.json")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def com_info(id):
    url = f"http://192.168.0.131:5000/company/{id}"
    file_path = 'text.json'

    try:
        response = requests.get(url)
        with open(file_path, 'w') as file:
            json.dump(response.json(), file, indent=4)
        print("Response has been written to input.json")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def chat_implementation(id, user_question):
    # return a
    url = f"http://192.168.0.131:5000/company/{id}/converse"
    payload = {
        "question": user_question
    }
    try:
        response = requests.post(url, json=payload)
        return response
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
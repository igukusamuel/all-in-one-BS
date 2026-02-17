import json

def load_users():
    with open("data/users.json", "r") as f:
        return json.load(f)

def authenticate(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None


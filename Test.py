users = {
    "test": {"password": "test", "score": 0, "questions_asked": []},
    "yossi": {"password": "123", "score": 50, "questions_asked": []},
    "master": {"password": "master", "score": 200, "questions_asked": []}
}
username = "test"
password = "test"
if username in users:
    if password == users[username]["password"]:
        print("heelo")

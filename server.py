##############################################################################
# server.py
##############################################################################

import socket
import chatlib
import random

# GLOBALS
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


def create_random_question(username):
    all_question = load_questions()
    listofusedquestions = users[username]["questions_asked"]
    listQ = []
    for key in all_question.keys():
        listQ.append(key)
    item_list = [e for e in listQ if e not in listofusedquestions]
    if len(item_list) != 0:
        random_num = random.choice(item_list)
        string = str(random_num) + chatlib.DATA_DELIMITER + all_question[random_num]["question"] \
                 + chatlib.DATA_DELIMITER + all_question[random_num]["answers"][0] + chatlib.DATA_DELIMITER + \
                 all_question[random_num]["answers"][1] + chatlib.DATA_DELIMITER + \
                 all_question[random_num]["answers"][2] + chatlib.DATA_DELIMITER + \
                 all_question[random_num]["answers"][3] + chatlib.DATA_DELIMITER + \
                 str(all_question[random_num]["correct"])
        users[username]["questions_asked"].append(random_num)
        return string
    else:
        return None


def handle_question_message(conn, username):
    question = create_random_question(username)
    if question is None:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER['noquestions_msg'], "")
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER['question_msg'], question)


def handle_answer_message(conn, username, answer):
    global users
    all_questions = load_questions()
    real_answer_for_question = all_questions[int(answer.split("#")[0])]["correct"]
    if str(real_answer_for_question) == answer.split("#")[1]:
        updated_score = 5 + users[username]["score"]
        users[username].update({"score": updated_score})
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER['correct_msg'], "")
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER['wrong_msg'], real_answer_for_question)


def build_and_send_message(conn, code, msg):
    full_msg = chatlib.build_message(code, msg)
    conn.send(full_msg.encode('utf-8'))


def recv_message_and_parse(conn):
    data = conn.recv(10021).decode()
    if len(data) == 0:
        return
    cmd, msg = chatlib.parse_message(data)
    if cmd != chatlib.ERROR_RETURN or msg != chatlib.ERROR_RETURN:
        # print(f"The server sent: {data}")
        # print(f"Interpretation:\nCommand: {cmd}, message: {msg}")
        return cmd, msg
    else:
        return chatlib.ERROR_RETURN, chatlib.ERROR_RETURN


# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
        0: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        1: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
            "correct": 3}
    }

    return questions


def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    users = {
        "test": {"password": "test", "score": 52, "questions_asked": []},
        "yossi": {"password": "123", "score": 50, "questions_asked": []},
        "master": {"password": "master", "score": 200, "questions_asked": []},
        "a": {"password": "a", "score": 123, "questions_asked": []}
    }
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    server_socket = socket.socket()
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(1)
    server_socket, address = server_socket.accept()
    return server_socket


def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER['error_msg'], error_msg)


# Implement code ...
def handle_logged_message(conn, username):
    global logged_users
    list_logged = list(logged_users.values())
    string_logged = ",".join([str(item) for item in list_logged])
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER['logged_msg'], string_logged)


def handle_getscore_message(conn, username):
    global users
    print("score: ", users[username]["score"])
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER['yourscore_msg'], users[username]["score"])


# Implement this in later chapters


def handle_logout_message(conn):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users
    del logged_users[conn.getpeername()]


def handle_all_score_message(conn, username):
    global users
    print("you ", users)
    list_of_score = {}
    for names in users:
        list_of_score.update({names: users[names]["score"]})
    string = ''
    for key, value in sorted(list_of_score.items(), key=lambda kv: kv[1], reverse=True):
        string += key + " " + str(value) + "\n"
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER['highscore_msg'], string)


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users
    global logged_users  # To be used later

    username, password = data.split("#")[0], data.split("#")[1]
    if username in users:
        if password == users[username]["password"]:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
            logged_users.update({conn.getpeername(): username})
            return
        else:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER['login_failed_msg'], "Error! Password does not match")
            print("Error! Password does not match")
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER['login_failed_msg'], "Error! Username does not exist")
        print("Error! Username does not exist")


# Implement code ...


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users  # To be used later

    if cmd == "LOGIN" and conn.getpeername() not in logged_users:
        handle_login_message(conn, data)
    elif cmd == "MY_SCORE" and conn.getpeername() in logged_users:
        handle_getscore_message(conn, logged_users[conn.getpeername()])
    elif cmd == 'LOGOUT' and conn.getpeername() in logged_users:
        handle_logout_message(conn)
    elif cmd == "GET_QUESTION" and conn.getpeername() in logged_users:
        handle_question_message(conn, logged_users[conn.getpeername()])
    elif cmd == "SEND_ANSWER" and conn.getpeername() in logged_users:
        handle_answer_message(conn, logged_users[conn.getpeername()], data)
    elif cmd == "LOGGED" and conn.getpeername() in logged_users:
        handle_logged_message(conn, logged_users[conn.getpeername()])
    elif cmd == 'HIGHSCORE' and conn.getpeername() in logged_users:
        handle_all_score_message(conn, logged_users[conn.getpeername()])


# Implement code ...


def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    server_socket = setup_socket()
    print('server is up at : ', SERVER_IP, SERVER_PORT)
    print("Welcome to Trivia Server!")
    global users
    global questions
    users = load_user_database()
    while True:
        cmd, msg = recv_message_and_parse(server_socket)
        print("= ", cmd, " = ", msg)
        handle_client_message(server_socket, cmd, msg)
        if cmd == "LOGOUT":
            server_socket = setup_socket()


# Implement code ...


if __name__ == '__main__':
    main()
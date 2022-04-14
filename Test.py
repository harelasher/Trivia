import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

def get_logged_users(conn):
    msg_code, msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["getlogged_msg"], "")
    return msg

def get_highscore(conn):
    msg_code, msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["gethighscore_msg"], "")
    return msg


def get_score(conn):
    msg_code, msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["getscore_msg"], "")
    return msg


# HELPER SOCKET METHODS
def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    msg_code, msg = recv_message_and_parse(conn)
    return msg_code, msg


def build_and_send_message(conn, code, msg):  # DONE
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), msg (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(code, msg)
    print("full message: ", full_msg)
    conn.send(full_msg.encode('utf-8'))


def recv_message_and_parse(conn):  # don't know??
    """
    Receives a new message from given socket.
    Prints debug info, then parses the message using chatlib.
    Parameters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    data = conn.recv(10021).decode()
    cmd, msg = chatlib.parse_message(data)
    if cmd != chatlib.ERROR_RETURN or msg != chatlib.ERROR_RETURN:
        # print(f"The server sent: {data}")
        # print(f"Interpretation:\nCommand: {cmd}, message: {msg}")
        return cmd, msg
    else:
        return chatlib.ERROR_RETURN, chatlib.ERROR_RETURN


def connect():  # DONE
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(msg):  # DONE??
    print(msg)
    exit()


def login(conn):  # DONE
    print("--Login--")
    while True:
        username = input("Please enter username: ")
        password = input("Please enter password: ")
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], username+chatlib.DATA_DELIMITER+password)
        msg = conn.recv(1024)
        if b"LOGIN_OK" in msg:
            print("--Logged in--")
            return
        print("--Couldn't Login Try Again--")


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")


def main():
    # Implement code
    UsedSocket = connect()
    login(UsedSocket)
    while True:
        print("Please choose an option [h,l,m,q,t]")
        print("h: Get high score\nl: Get logged users\nm: Get my score\nt: Play a trivia question\nq: Quit")
        function = input().lower()
        if "q" == function:
            logout(UsedSocket)
            print("goodbye!")
            return
        elif "m" == function:
            score = get_score(UsedSocket)
            print("your score: ", score)
        elif "h" == function:
            HighScore = get_highscore(UsedSocket)
            print(HighScore)
        elif "l" == function:
            Users = get_logged_users(UsedSocket)
            print(Users)


if __name__ == '__main__':
    main()

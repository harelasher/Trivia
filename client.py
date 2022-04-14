import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):  # DONE
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), msg (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(code, msg)
    print(full_msg)
    conn.send(full_msg.encode('utf-8'))


def recv_message_and_parse(conn):  # dont know??
    """
    Recieves a new message from given socket.
    Prints debug info, then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    msg = conn.recv(1024)
    cmd, msg = chatlib.parse_message(msg)
    return cmd, msg


def connect():  # DONE
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(msg):  # DONE??
    print(msg)
    exit()


def login(conn):  # DONE
    while True:
        username = input("Please enter username: ")
        password = input("Please enter password: ")
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], username+chatlib.DATA_DELIMITER+password)
        msg = conn.recv(1024)
        if b"LOGIN_OK" in msg:
            return


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")


def main():
    # Implement code
    x = connect()
    login(x)
    logout(x)


if __name__ == '__main__':
    main()

import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):  # DONE??
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), msg (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(code, msg)
    print(full_msg)
    conn.send(full_msg.encode('utf-8'))


def recv_message_and_parse(conn):
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
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # בונה את הלקוח
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(msg):  # DONE??
    print(msg)
    exit()


def login(conn):
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")

        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")

        msg = conn.recv(1024)
        print(msg)
        if len(msg) == 0:
            return


def logout(conn):
    print("cancer")


def main():
    # Implement code
    x = connect()
    login(x)
    logout(x)


if __name__ == '__main__':
    main()

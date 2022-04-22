def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    server_socket = socket.socket()
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    server_socket, address = server_socket.accept()
    return server_socket


while True:
    cmd = None
    msg = None
    try:
        cmd, msg = recv_message_and_parse(server_socket)
    except:
        server_socket = setup_socket()
    print("= ", cmd, " = ", msg)
    handle_client_message(server_socket, cmd, msg)
    if cmd == "LOGOUT":
        server_socket = setup_socket()


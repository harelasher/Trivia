import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678  # פורט השרת


def check_answer():  # פונקצית לבדיקת התשובה של המשתמש
    while True:
        answer = input("answer (1-4): ").lower()
        if answer.isnumeric():
            answer = int(answer)
            if 1 <= answer <= 4:
                return str(answer)


def play_question(conn):  # פונקציה להצגת השאלה
    try:
        # שולח לשרת בקשה לשאלה
        msg_code, question = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["getquestion_msg"], "")
        parts_of_question = question.split("#")  # חוצה את השאלה לפי "#"
        if msg_code != 'NO_QUESTIONS':  # אם יש עוד שאלות לשאול את המשתמש
            print(parts_of_question[1])
            print("1. ", parts_of_question[2])
            print("2. ", parts_of_question[3])
            print("3. ", parts_of_question[4])
            print("4. ", parts_of_question[5])
            # מדפיס את השאלה והתשובות
            answer = check_answer()
            msg_code, msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["sendanswer_msg"],
                                                  parts_of_question[0] + chatlib.DATA_DELIMITER + answer)
            print(msg_code)
            if msg_code != "CORRECT_ANSWER":
                print("right anwswer: " + msg)
        else:
            print("no more questions ")
    except NameError:
        print("\nerror")


def get_logged_users(conn):  # פונקציה לקבלת המשתמשים המחוברים
    msg_code, msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["getlogged_msg"], "")
    return "logged users: " + msg


def get_highscore(conn):  # פונקציה לקבלת כל המשתמשים עם הנקודות שלהם
    msg_code, msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["gethighscore_msg"], "")
    return msg


def get_score(conn):  # פונקציה לקבלת הנקודות של המשתמש
    msg_code, msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["getscore_msg"], "")
    return msg


# HELPER SOCKET METHODS
def build_send_recv_parse(conn, code, data):  # מחבר את שתי הפונקציה, יוצר הודעה שולח אותה ומחכה לתשובה
    build_and_send_message(conn, code, data)
    msg_code, msg = recv_message_and_parse(conn)
    return msg_code, msg


def build_and_send_message(conn, code, msg):  # פונקציה לבניית הודעה ושליחה לשרת
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), msg (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(code, msg)  # בונה את ההודעה
    conn.send(full_msg.encode('utf-8'))  # ושולח את ההודעה


def recv_message_and_parse(conn):  # פונקציה לקבלת מידע מהשרת
    """
    Receives a new message from given socket.
    Prints debug info, then parses the message using chatlib.
    Parameters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    data = conn.recv(10021).decode()  # הלקוח קולט מידע
    cmd, msg = chatlib.parse_message(data)  # מנתח את המידע
    if cmd != chatlib.ERROR or msg != chatlib.ERROR:  # אם המידע הוא לא שגיאה
        # print(f"The server sent: {data}")
        # print(f"Interpretation:\nCommand: {cmd}, message: {msg}")
        return cmd, msg
    else:
        return chatlib.ERROR, chatlib.ERROR


def connect():  # פונקציה חיבור לשרת
    # Implement Code
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def login(conn):  # פונקציה כניסה למשחק
    print("--Login--")
    while True:
        username = input("Please enter username: ")  # בקשת שם משתמש
        password = input("Please enter password: ")  # בקשת סיסמה
        #  שליחת הודעה כניסה לשרת
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], username + chatlib.DATA_DELIMITER + password)
        cmd, msg = recv_message_and_parse(conn)  # קבלת הודעה מהשרת
        if "LOGIN_OK" in cmd:  # אם השרת הכניס את המשתמש אז מוציא אותו מהפונקציה הזאת
            print("--Logged in--")
            return
        print(msg)
        print("--Try Again--")


def logout(conn):  # פונקציה לשליחה לשרת הודעת יציאה מהמשחק
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT['logout_msg'], "")


def main():
    # Implement code
    UsedSocket = connect()  # מחבר את הלקוח לשרת
    login(UsedSocket)  # שולח הודעת לוגאין
    while True:
        print("Please choose an option [h,l,m,q,t]")
        print("h: Get high score\nl: Get logged users\nm: Get my score\nt: Play a trivia question\nq: Quit")
        function = input().lower()  # תשובת הלקוח
        if "q" == function:  # לצאת מהמשחק
            logout(UsedSocket)
            print("goodbye!")
            return
        elif "m" == function:  # להראות את הנקודות של הלקוח
            score = get_score(UsedSocket)
            print("your score: ", score)
        elif "h" == function:  # להראות את הנקודות של כל המשתמשים
            HighScore = get_highscore(UsedSocket)
            print(HighScore)
        elif "l" == function:  # להראות את כל הלקוחות במשחק
            Users = get_logged_users(UsedSocket)
            print(Users)
        elif "t" == function:  # לענות על שאלה
            play_question(UsedSocket)


if __name__ == '__main__':
    main()

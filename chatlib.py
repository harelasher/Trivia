CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = '#'
PROTOCOL_CLIENT = {'login_msg': 'LOGIN',
                   'logout_msg': 'LOGOUT',
                   'getscore_msg': 'MY_SCORE',
                   'getlogged_msg': 'LOGGED',
                   'gethighscore_msg': 'HIGHSCORE',
                   'getquestion_msg': 'GET_QUESTION',
                   'sendanswer_msg': 'SEND_ANSWER'}
PROTOCOL_SERVER = {'login_ok_msg': 'LOGIN_OK',
                   'login_failed_msg': 'ERROR',
                   'yourscore_msg': 'YOUR_SCORE',
                   'highscore_msg': 'ALL_SCORE',
                   'logged_msg': 'LOGGED_ANSWER',
                   'correct_msg': 'CORRECT_ANSWER',
                   'wrong_msg': 'WRONG_ANSWER',
                   'question_msg': 'YOUR_QUESTION',
                   'error_msg': 'ERROR',
                   'noquestions_msg': 'NO_QUESTIONS'}
ERROR = None


def build_message(cmd, data):
    """
        Gets command name (str) and data field (str) and creates a valid protocol message
        Returns: str, or None if error occured
        """
    if type(data) is int:
        data = str(data)

    data_length = len(data)
    cmd_length = len(cmd)
    if data_length > MAX_DATA_LENGTH:
        return ERROR
    elif cmd_length > CMD_FIELD_LENGTH:
        return ERROR
    else:
        padded_cmd = cmd.strip().ljust(CMD_FIELD_LENGTH)
        padded_length = str(data_length).zfill(LENGTH_FIELD_LENGTH)
        full_msg = f"{padded_cmd}{DELIMITER}{padded_length}{DELIMITER}{data}"
        return full_msg


def parse_message(full_msg):
    """
        Parses protocol message and returns command name and data field
        Returns: cmd (str), data (str). If some error occured, returns None, None
        """
    if len(full_msg) < CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1:
        return ERROR, ERROR
    cmd_str = full_msg[0:CMD_FIELD_LENGTH]
    length = full_msg[CMD_FIELD_LENGTH + 1:CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH]
    if full_msg[CMD_FIELD_LENGTH] != DELIMITER or full_msg[(CMD_FIELD_LENGTH + LENGTH_FIELD_LENGTH + 1)] != DELIMITER:
        return ERROR, ERROR
    elif not length.strip().isdigit():
        return ERROR, ERROR
    length = int(length)
    data_str = full_msg[MSG_HEADER_LENGTH:MSG_HEADER_LENGTH + length]
    if not len(data_str) == length:
        return ERROR, ERROR
    else:
        return cmd_str.strip(), data_str


def split_data(msg, expected_fields):
    """
        Helper method. gets a string and number of expected fields in it. Splits the string
        using protocol's data field delimiter (|#) and validates that there are correct number of fields.
        Returns: list of fields if all ok. If some error occured, returns None
        """
    splitted = msg.split(DATA_DELIMITER)
    if len(splitted) == expected_fields:
        return splitted
    else:
        return


def join_data(msg_fields):
    """
        Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
        Returns: string that looks like cell1#cell2#cell3
        """
    return DATA_DELIMITER.join(msg_fields)

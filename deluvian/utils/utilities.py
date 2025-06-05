import os

BYTES_IN_SHA1 = 20
ENCODING = "utf-8"


class BDecoder:

    def __init__(self, input_file):
        self._input_file = input_file
        self._current_position = 0

    def _read_bytes(self, n):
        self._input_file.seek(self._current_position)
        ret = self._input_file.read(n)
        self._current_position = self._current_position + n
        return ret

    # Reads a given number of characters and returns it as a string.
    def _read_number_until(self, c):
        ret = ""
        while True:
            v = self._read_bytes(1).decode('ascii')
            # Consider not appending to a string for faster implementation
            if v.isdigit() or v == '-':
                ret += v
            else:
                if v != c:
                    errmsg = "Error: Expected '%s', got '%s'." % (c, v)
                    raise ValueError(errmsg)
                return ret

    def _read_dict(self):
        ret = {}
        while True:
            key = self.read_value()
            if key is None:
                return ret
            value = self.read_value()
            ret[key] = value

    def _read_list(self):
        ret = []
        while True:
            v = self.read_value()
            if v is not None:
                ret += [v]
            else:
                return ret

    def _read_string(self, previous):
        t = previous + self._read_number_until(":")
        ret = self._read_bytes(int(t))
        return ret

    def read_value(self):
        t = self._read_bytes(1).decode('ascii')
        if t == 'e':
            return None
        elif t == 'd':
            return self._read_dict()
        elif t.isdigit():
            return self._read_string(previous=t)
        elif t == 'l':
            return self._read_list()
        elif t == 'i':
            return self._read_number_until('e')
        elif t == '':  # Reached end of file?
            return None
        else:
            raise ValueError("Unexpected type: %s" % t)

    def read_next(self):
        return self.read_value()

    def reset_position(self):
        self._current_position = 0


# def is_delimiter(input):
#     output = False
#     if input == DICTIONARY_DELIMITER:
#         output = True
#     elif input == END_DELIMITER:
#         output == True
#     elif input == INTEGER_DELIMITER:
#         output = True
#     elif input == LIST_DELIMITER:
#         output = True
#     # else:
#     #     output = False
#
# def parse_bencode(input_file):
#     index = 0
#     is_inside_value = False
#     temporary = []
#     for input_byte in input_file:
#         if not is_inside_value:
#             if is_delimiter(input_byte):
#                 is_inside_value = True
#         else:
#             if is_delimiter(input_byte):
#                 print(temporary)
#                 temporary = []
#             else:
#                 temporary.append(input_file)

def bdecode_alt(input_file):
    bdecoder = BDecoder(input_file)
    output = []
    while True:
        temporary = bdecoder.read_next()
        if temporary is None:
            break
        else:
            output.append(temporary)
    return output


def bdecode(filename):
    filehandle = open(filename, "rb")
    file_output = bdecode_alt(filehandle)
    return file_output


def pretty_print(d, indentation=0, is_indented=True):
    if isinstance(d, list):
        for value in d:
            pretty_print(value, indentation + 1)
    elif isinstance(d, dict):
        print("")
        for key, value in d.items():
            print('\t' * (indentation + 1) + str(key), end="")
            print(" : ", end="")
            pretty_print(value, indentation + 1, is_indented=False)
    else:
        if is_indented:
            print('\t' * (indentation + 1), end="")
        print(str(d))


def pretty_print_alt(d, indentation=0, is_indented=True):
    output = ""
    if isinstance(d, list):
        for value in d:
            output += pretty_print_alt(value, indentation + 1)
    elif isinstance(d, dict):
        for key, value in d.items():
            output += ('\t' * (indentation + 1) + str(key))
            output += " : "
            output += pretty_print_alt(value, indentation + 1, is_indented=False)
    else:
        if is_indented:
            output += ('\t' * (indentation + 1))
        output += (str(d) + '\n')
    return output


def pretty_print_torrent(output, is_pieces_included=False):
    information = output[0][b'info'][b'pieces']
    information = ''.join('{:02x}'.format(x) for x in bytearray(information))
    information = information.upper()
    chunk_size = BYTES_IN_SHA1
    chunks = int(len(information) / chunk_size)
    information = [information[i:(i + chunk_size)] + '\n' for i in range(0, chunks, chunk_size)]
    if is_pieces_included:
        output[0][b'info'][b'pieces'] = information
    else:
        output[0][b'info'].pop(b'pieces')
    return pretty_print_recursive(output)


def pretty_print_recursive(d, indentation=0, is_indented=True):
    output = ""
    if isinstance(d, list):
        for value in d:
            output += pretty_print_recursive(value, indentation + 1)
    elif isinstance(d, dict):
        for key, value in d.items():
            if key == b'pieces':
                # output += ('\t' * (indentation + 1) + str(key))
                output += ('\t' * (indentation + 1) + key.decode(ENCODING))
                output += " : "
                if not isinstance(value, list):
                    value = ''.join('{:02x}'.format(x) for x in bytearray(value))
                output += pretty_print_recursive(value, indentation + 1, is_indented=False)
            else:
                # output += ('\t' * (indentation + 1) + str(key))
                output += ('\t' * (indentation + 1) + key.decode(ENCODING))
                output += " : "
                if isinstance(value, dict):
                    output += "\n"
                elif isinstance(value, list):
                    output += "\n"
                output += pretty_print_recursive(value, indentation + 1, is_indented=False)
    else:
        if is_indented:
            output += ('\t' * (indentation + 1))
        # output += (str(d) + '\n')
        if type(d) == str:
            output += (d + '\n')
        else:
            output += (d.decode(ENCODING) + '\n')
    return output


ROOT_INDEX = 0
FILENAME_INDEX = 1


def print_tuple_list(tuple_list, is_custom_format=True):
    input_list = []
    if is_custom_format:
        for x in tuple_list:
            root = x[ROOT_INDEX]
            filename = x[FILENAME_INDEX]
            input_list.append(os.path.join(root, filename))
    else:
        for x in tuple_list:
            input_list.append(''.join(x))
    return '\n'.join(input_list)

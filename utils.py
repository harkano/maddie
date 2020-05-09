import json

MAX_POSITIVE_MOD = 4
MIN_NEGATIVE_MOD = 3
SUM = '+'
SUB = '-'

def get_modified_num(mod, num):
    if mod == SUM: return min(num, MAX_POSITIVE_MOD)
    if mod == SUB: return -1 * min(num, MIN_NEGATIVE_MOD)
    return num


def get_moves(language = 'en'):
    ##Load in the existing moves
    input_file = open (f'language_files/{language}.json')
    json_array = json.load(input_file)

    return json_array
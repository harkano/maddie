MAX_POSITIVE_MOD = 4
MIN_NEGATIVE_MOD = 3
SUM = '+'
SUB = '-'

def get_modified_num(mod, num):
    if mod == SUM: return min(num, MAX_POSITIVE_MOD)
    if mod == SUB: return -1 * min(num, MIN_NEGATIVE_MOD)
    return num

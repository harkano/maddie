import re

from playbooks import get_playbook_names, get_playbook_list

COMMA_SEPARATOR = ', '
PLUS = '+'

def compare_move_to_playbook(move, playbook_name):
    if 'playbook' in move:
        return move['playbook'] == playbook_name

    return False


def join_with_commas(array_to_join, field):
    result = ''
    index = 1

    for joinable in array_to_join:
        result = result + joinable[field]
        if index != len(array_to_join):
            result = result + COMMA_SEPARATOR
            index = index + 1

    return result


def join_with_detail(array_to_join):
    response = '**Name - description, keyword, label**\n'

    for p in array_to_join:
        response = response + p['capital'].capitalize() + " - " + p['description'] + \
            COMMA_SEPARATOR + p['shortName'] + \
            COMMA_SEPARATOR + p['label'] + "\n "

    return response


def get_playbook_field(command):
    playbook_list = get_playbook_list()

    if command in playbook_list:
        return command

    if command.startswith('moves'):
        return 'basic'

    if command.startswith('adult'):
        return 'adult'

    return ''


def parse_command(command):
    raw_command = command[1:]
    has_plus = PLUS in raw_command

    if has_plus:
      command_name = raw_command.split(PLUS)[0]

      return command_name, True

    return raw_command, False

def get_unknown_playbook_response():
    response = "Sorry, I couldn't find that playbook, the available playbooks are:"
    for playbook in get_playbook_names():
        response = response + playbook

    response = response + "\nType an exclamation sign and one of the names in lowercase and without the 'The', basic or adult\ne.g.: !beacon, !moves, !adult"

    # return response #changing this as we need to be polite to other bots, there's a lot of them
    return 0


def get_moves(message, moves_array):
    content = message.content

    type_of_command, show_detail = parse_command(content)

    playbook_field = get_playbook_field(type_of_command)

    if playbook_field:
        moves_by_playbook = list(filter(lambda move_dict: compare_move_to_playbook(
            move_dict, playbook_field), moves_array['moves']))

        if not len(moves_by_playbook):
            return get_unknown_playbook_response()

        if show_detail:
            return join_with_detail(moves_by_playbook)

        return join_with_commas(moves_by_playbook, 'shortName')

    return None

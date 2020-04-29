import re

from playbooks import get_playbook_names, get_playbook_list

COMMA_SEPARATOR = ', '


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


def get_playbook_field(command):
    playbook_list = get_playbook_list()

    if command in playbook_list:
        return command

    if command.startswith('moves'):
        return 'basic'

    if command.startswith('adult'):
        return 'adult'

    return ''


def get_unknown_playbook_response():
    response = "Sorry, I couldn't find that playbook, the available playbooks are:"
    for playbook in get_playbook_names():
        response = response + playbook
    
    response = response + "\nType an exclamation sign and one of the names in lowercase and without the 'The', basic or adult\ne.g.: !beacon, !moves, !adult"

    return response


def get_moves(message, moves_array):
    content = message.content

    type_of_command = content[1:]
    print(type_of_command)

    if type_of_command.startswith('moves+'):
        basic_moves_list = list(filter(lambda move_dict: compare_move_to_playbook(move_dict, 'basic'), moves_array['moves']))

        response = '**Name - description, keyword, label**\n'
        for p in basic_moves_list:
          response = response + p['capital'].capitalize() + " - " + p['description'] + COMMA_SEPARATOR + p['shortName'] + COMMA_SEPARATOR + p['label'] + "\n "

        return response

    playbook_field = get_playbook_field(type_of_command)

    if playbook_field:
        moves_by_playbook = list(filter(lambda move_dict: compare_move_to_playbook(move_dict, playbook_field), moves_array['moves']))
        
        if not len(moves_by_playbook):
          return get_unknown_playbook_response()

        return join_with_commas(moves_by_playbook, 'shortName')

    return None

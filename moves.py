import re

from playbooks import get_playbook_names

MOVE_BY_PLAYBOOK_REGEX = r'!moves-(\w)'
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


def get_moves(message, moves_array):
    content = message.content

    if re.search(MOVE_BY_PLAYBOOK_REGEX, content):
        playbook_name = content.split('-')[1]
        moves_by_playbook = list(filter(lambda move_dict: compare_move_to_playbook(move_dict, playbook_name), moves_array['moves']))
        
        if not len(moves_by_playbook):
          response = "Sorry, I couldn't find that playbook, the available playbooks are:"
          for playbook in get_playbook_names():
            response = response + playbook
          
          response = response + "\nAdd one of the names in lowercase and without the 'The', basic or adult\ne.g.: !moves-beacon, !moves-basic, !moves-adult"

          return response

        return join_with_commas(moves_by_playbook, 'shortName')

    if content.startswith("!moves+"):
        response = '**Name - description, keyword, label**\n'
        for p in moves_array['moves']:
          response = response + p['capital'].capitalize() + " - " + p['description'] + COMMA_SEPARATOR + p['shortName'] + COMMA_SEPARATOR + p['label'] + "\n "
        
        return response

    if content.startswith("!moves"):
        response = ''

        return join_with_commas(moves_array['moves'], 'shortName')

    return None

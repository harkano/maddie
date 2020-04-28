PLAYBOOK_LIST = ['beacon', 'bull', 'delinquent', 'doomed', 'janus', 'legacy', 'nova', 'outsider', 'protege', 'transformed']

def get_playbook_list ():
    return PLAYBOOK_LIST


def format_playbook_name (name):
    capitalized_name = name.capitalize()

    return f'\n• The {capitalized_name}'

def get_playbook_names ():
    return list(map(format_playbook_name, PLAYBOOK_LIST))
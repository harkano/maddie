import boto3
import json
from s3_utils import info_from_s3, get_s3_client, upload_to_s3, get_files_from_dir

LABELS = 'labels'
VALUE = 'value'
LOCKED = 'locked'
POTENTIAL = 'potential'
PENDING_ADVANCEMENTS = 'pendingAdvancements'
CONDITIONS = 'conditions'
MOVES = 'moves'
ADVANCEMENT = 'advancement'
MAX_LABEL_VALUE = 3
MIN_LABEL_VALUE = -2

# These are the auxiliar functions

def label_is_not_editable(label, value):
    locked = label[LOCKED]

    return locked or value == MAX_LABEL_VALUE or value == MIN_LABEL_VALUE


def get_label_has_border_value_text(label_name, label, direction):
    value = label[VALUE]
    locked = label[LOCKED]

    if locked:
        return f"Oh no, {label_name} is locked, this one can't change!"

    return f"Oh no, with a value of {value}, your {label_name} can't go {direction}! You get a condition!"


def format_labels(labels):
    response = "Your labels are:\n"

    for label in labels:
        name = label.capitalize()
        value = labels[label][VALUE]

        if labels[label][LOCKED]:
            is_locked = '[LOCKED]'
        else:
            is_locked = ''

        response = response + f'{name}: {value} {is_locked}\n'

    return response


def format_conditions(conditions):
    if not len(conditions):
        return "You don't have any condition marked"

    response = "You are:\n"

    for condition in conditions:
        if conditions[condition]:
            response = response + f"  - {condition}\n"

    return response


def get_condition_is_unchangable(is_marked):
    dont = ''
    if not is_marked:
        dont = "don't "
    
    return f"Oh, you {dont}have that condition marked."


def invert_condition(message, compare_to):
    key, content = get_key_and_content_from_message(message)
    condition_name = get_args_from_content(content)

    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if not char_info:
        return "I'm sorry but it appears you have no character created"

    conditions = char_info[CONDITIONS]

    if condition_name not in conditions:
        return f"Oh no, {condition_name} is not a valid condition"

    condition_to_mark = conditions[condition_name]

    if condition_to_mark == compare_to:
        return get_condition_is_unchangable(compare_to)

    char_info[CONDITIONS][condition_name] = compare_to

    upload_to_s3(char_info, key, s3_client)

    return format_conditions(char_info[CONDITIONS])


def format_moves(moves):
    return ''


def get_args_from_content(content):
    splited = content.split(" ")

    if len(splited) == 2:
        return splited[1]

    return splited[1:]


def get_key_and_content_from_message(message):
    key = f'{message.channel.id}/{message.author.id}'

    return key, message.content

# These are the functions that edit the data in the characters s3 file

def edit_labels(message):
    key, content = get_key_and_content_from_message(message)
    label_to_increase_name, label_to_decrease_name = get_args_from_content(content)

    if label_to_increase_name == label_to_decrease_name:
        return "The labels must be different, you must select one of your valid labels"

    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if not char_info:
        return "I'm sorry but it appears you have no character created"

    labels = char_info[LABELS]

    label_to_increase = labels[label_to_increase_name]
    label_to_increase_value = label_to_increase[VALUE]
    label_to_decrease = labels[label_to_decrease_name]
    label_to_decrease_value = label_to_decrease[VALUE]

    if label_is_not_editable(label_to_increase, label_to_increase_value):
        return get_label_has_border_value_text(label_to_increase_name, label_to_increase, 'up')

    if label_is_not_editable(label_to_decrease, label_to_decrease_value):
        return get_label_has_border_value_text(label_to_decrease_name, label_to_decrease, 'down')

    labels[label_to_increase_name][VALUE] = label_to_increase_value + 1
    labels[label_to_decrease_name][VALUE] = label_to_decrease_value - 1

    upload_to_s3(char_info, key, s3_client)

    return format_labels(labels)


def lock_label(message):
    key, content = get_key_and_content_from_message(message)
    label_to_lock_name = get_args_from_content(content)

    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if not char_info:
        return "I'm sorry but it appears you have no character created"

    labels = char_info[LABELS]
    label_to_lock = labels[label_to_lock_name]

    if label_to_lock[LOCKED]:
        return f"Oh no, {label_to_lock_name} is already locked, choose another one!"

    labels[label_to_lock_name][LOCKED] = True

    upload_to_s3(char_info, key, s3_client)

    return format_labels(labels)


def mark_potential(message):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if not char_info:
        return "I'm sorry but it appears you have no character created"

    potential = char_info[POTENTIAL]

    if potential == 4:
        char_info[POTENTIAL] = 0
        char_info[PENDING_ADVANCEMENTS] = char_info[PENDING_ADVANCEMENTS] + 1

        upload_to_s3(char_info, key, s3_client)
        return f"Nice, you can now do {char_info[PENDING_ADVANCEMENTS] + 1} advancements"

    char_info[POTENTIAL] = potential + 1

    upload_to_s3(char_info, key, s3_client)
    return f"Nice, you have {potential + 1} potential marked"


def mark_condition(message):
    return invert_condition(message, True)


def clear_condition(message):
    return invert_condition(message, False)


def create_character(message):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()

    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if char_info:
        return "It seems you already have a character"

    playbook_name, character_name, player_name, label_to_increase = get_args_from_content(content)
    file_list = get_files_from_dir('playbooks', s3_client)
    template_key = f'playbooks/{playbook_name}'

    matching_files = list(filter(lambda file_info: file_info["Key"] == f'{template_key}.json', file_list["Contents"]))

    if not len(matching_files):
        return f"It seems I don't have a template for a playbook called {playbook_name}"

    print(matching_files)
    template = info_from_s3(template_key, s3_client)

    template[LABELS][label_to_increase][VALUE] = template[LABELS][label_to_increase][VALUE] + 1
    template['characterName'] = character_name
    template['playerName'] = player_name

    upload_to_s3(template, key, s3_client)

    formated_playbook_name = playbook_name.capitalize()
    return f"Congratulations {character_name}, The {formated_playbook_name} on joining the team!"

# These are the functions that get the data in the characters s3 file

def get_labels(message):
    key = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if not char_info:
        return "I'm sorry but it appears you have no character created"

    return format_labels(char_info[LABELS])


def get_conditions(message):
    key = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if not char_info:
        return "I'm sorry but it appears you have no character created"

    return format_conditions(char_info[CONDITIONS])


def get_potential(message):
    key = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if not char_info:
        return "I'm sorry but it appears you have no character created"

    potential = char_info[POTENTIAL]

    return f"You have {potential} potential marked"

def get_moves(message):
    key = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if not char_info:
        return "I'm sorry but it appears you have no character created"

    return format_moves(char_info[MOVES])

def get_pending_advancements(message):
    key = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if not char_info:
        return "I'm sorry but it appears you have no character created"
    pending_advancements = char_info[PENDING_ADVANCEMENTS]

    return f"You have {pending_advancements} unresolved advancements"

def get_advancements(message):
    key = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)
    if not char_info:
        return "I'm sorry but it appears you have no character created"

    return ""
    # return format_advancements(char_info[ADVANCEMENT])
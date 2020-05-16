import boto3
import json
from s3_utils import info_from_s3, get_s3_client, upload_to_s3, get_files_from_dir
from language_handler import get_translation
from utils import get_moves as get_moves_json_array

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
PLAYBOOK_INTERACTIONS = 'playbook_interactions'
# These are the auxiliar functions

def label_is_not_editable(label, border_value):
    locked = label[LOCKED]
    value = label[VALUE]

    return locked or value == border_value


def get_label_has_border_value_text(label_name, label, direction, lang):
    value = label[VALUE]
    locked = label[LOCKED]

    if locked:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.is_locked')(get_translation(lang, f'labels.{label_name}'))

    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.value_is_in_border')(value, get_translation(lang, f'labels.{label_name}'), direction)


def format_labels(labels, lang):
    response = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.labels_base')

    for label in labels:
        name = get_translation(lang, f'labels.{label}').capitalize()
        value = labels[label][VALUE]

        if labels[label][LOCKED]:
            is_locked = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.locked')
        else:
            is_locked = ''

        response = response + f'{name}: {value} {is_locked}\n'

    return response


def format_conditions(conditions, lang):
    if not len(conditions):
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.condition_not_marked')

    response = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.youre')

    for condition in conditions:
        if conditions[condition]:
            response = response + f"  - {get_translation(lang, f'conditions.{condition}')}\n"

    return response


def get_condition_is_unchangable(is_marked, lang):
    dont = ''
    if not is_marked:
        dont = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.dont')
    
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.condition_status')(dont)


def invert_condition(message, compare_to, lang):
    key, content = get_key_and_content_from_message(message)
    condition_name_og = get_args_from_content(content)
    condition_name = get_translation(lang, f'inverted_conditions.{condition_name_og}')

    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    conditions = char_info[CONDITIONS]

    if condition_name not in conditions:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.invalid_condition')

    condition_to_mark = conditions[condition_name]

    if condition_to_mark == compare_to:
        return get_condition_is_unchangable(compare_to, lang)

    char_info[CONDITIONS][condition_name] = compare_to

    upload_to_s3(char_info, key, s3_client)

    return format_conditions(char_info[CONDITIONS], lang)


def format_moves(moves):
    return ''


def get_args_from_content(content):
    from tssplit import tssplit
    #splited = content.split(" ")
    splited = tssplit(content, quote='"', delimiter=' ')
    if len(splited) == 2:
        return splited[1]

    return splited[1:]


def get_key_and_content_from_message(message):
    key = f'{message.channel.id}/{message.author.id}'

    return f'adventures/{key}', message.content


def format_advance_list(advance_list, list_name, lang):
    response = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.{list_name}') + '\n'

    for advance_key in advance_list:
        advance = advance_list[advance_key]
        description = advance['description']
        response = response + '• '
        if advance['taken']:
            response = response + get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.taken')

        response = response + get_translation(lang, f'playbooks.advances.{description}') + '\n'

    return response


def format_advancements(advancements, lang):
    basic = advancements['basic']
    advanced = advancements['advanced']

    formated_basic = format_advance_list(basic, 'basic', lang)
    formated_advanced = format_advance_list(advanced, 'advanced', lang)

    return formated_basic + formated_advanced


# These are the functions that edit the data in the characters s3 file

def edit_labels(message, lang):
    key, content = get_key_and_content_from_message(message)
    label_to_increase_name_og, label_to_decrease_name_og = get_args_from_content(content)

    if label_to_increase_name_og == label_to_decrease_name_og:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.different_labels')

    label_to_increase_name = get_translation(lang, f'inverted_labels.{label_to_increase_name_og}')
    label_to_decrease_name = get_translation(lang, f'inverted_labels.{label_to_decrease_name_og}')

    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    labels = char_info[LABELS]

    label_to_increase = labels[label_to_increase_name]
    label_to_increase_value = label_to_increase[VALUE]
    label_to_decrease = labels[label_to_decrease_name]
    label_to_decrease_value = label_to_decrease[VALUE]

    if label_is_not_editable(label_to_increase, MAX_LABEL_VALUE):
        up = get_translation(lang,  f'{PLAYBOOK_INTERACTIONS}.up')
        return get_label_has_border_value_text(label_to_increase_name, label_to_increase, up, lang)

    if label_is_not_editable(label_to_decrease, MIN_LABEL_VALUE):
        down = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.down')
        return get_label_has_border_value_text(label_to_decrease_name, label_to_decrease, down, lang)

    labels[label_to_increase_name][VALUE] = label_to_increase_value + 1
    labels[label_to_decrease_name][VALUE] = label_to_decrease_value - 1

    upload_to_s3(char_info, key, s3_client)

    return format_labels(labels, lang)


def lock_label(message, lang):
    key, content = get_key_and_content_from_message(message)
    label_to_lock_name_og = get_args_from_content(content)
    label_to_lock_name = get_translation(lang, f'inverted_labels.{label_to_lock_name_og}')

    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    labels = char_info[LABELS]
    label_to_lock = labels[label_to_lock_name]

    if label_to_lock[LOCKED]:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.already_locked')(get_translation(lang, f'labels.{label_to_lock_name}'))

    labels[label_to_lock_name][LOCKED] = True

    upload_to_s3(char_info, key, s3_client)

    return format_labels(labels, lang)


def mark_potential(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    potential = char_info[POTENTIAL]

    if potential == 4:
        char_info[POTENTIAL] = 0
        char_info[PENDING_ADVANCEMENTS] = char_info[PENDING_ADVANCEMENTS] + 1

        upload_to_s3(char_info, key, s3_client)
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.congrats_pending_advancements')(char_info[PENDING_ADVANCEMENTS])

    char_info[POTENTIAL] = potential + 1

    upload_to_s3(char_info, key, s3_client)
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.congrats_potential')(potential)


def mark_condition(message, lang):
    return invert_condition(message, True, lang)


def clear_condition(message, lang):
    return invert_condition(message, False, lang)


def create_character(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()

    char_info = info_from_s3(key, s3_client)
    if char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.existing_character')

    playbook_name, character_name, player_name, label_to_increase = get_args_from_content(content)
    file_list = get_files_from_dir('playbooks', s3_client)
    template_key = f'playbooks/{playbook_name}'

    matching_files = list(filter(lambda file_info: file_info["Key"] == f'{template_key}.json', file_list["Contents"]))

    if not len(matching_files):
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_template')

    template = info_from_s3(template_key, s3_client)

    template[LABELS][label_to_increase][VALUE] = template[LABELS][label_to_increase][VALUE] + 1
    template['characterName'] = character_name
    template['playerName'] = player_name

    upload_to_s3(template, key, s3_client)

    formated_playbook_name = playbook_name.capitalize()
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.congrats_on_creation')(character_name, formated_playbook_name)


def add_move_from_your_playbook(message, lang):
    key, content = get_key_and_content_from_message(message)
    move_name = get_args_from_content(content)

    # TODO get the move id
    moves_array = get_moves_json_array(lang)['moves']
    move_list = list(filter(lambda move_dict: move_dict['shortName'] == move_name, moves_array))

    if not len(move_list):
        # TODO add to dict
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_moves_pb')

    id = move_list[0]['id']

    s3_client = get_s3_client()
    char_info = info_from_s3(f'adventures/{key}', s3_client)

    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    move = list(filter(lambda dic: dic["id"] == id, char_info['moves']))[0]
    if move['picked']:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.move_already_taken')

    move["picked"] = True

    upload_to_s3(char_info, key, s3_client)

    return 'format_conditions(char_info[CONDITIONS], lang)'


# These are the functions that get the data in the characters s3 file

def get_labels(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    return format_labels(char_info[LABELS], lang)


def get_conditions(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    return format_conditions(char_info[CONDITIONS], lang)


def get_potential(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    potential = char_info[POTENTIAL]

    return get_translation(lany,  f'{PLAYBOOK_INTERACTIONS}.potential')(potential)


def get_moves(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    return format_moves(char_info[MOVES])


def get_pending_advancements(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')
    pending_advancements = char_info[PENDING_ADVANCEMENTS]

    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.pending_advancements')(pending_advancements)


def get_advancements(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    return format_advancements(char_info[ADVANCEMENT], lang)
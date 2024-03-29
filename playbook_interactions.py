# import boto3 # This is unused in this file.
import json
from storage import info_from_s3, get_s3_client, upload_to_s3, get_files_from_dir, s3_delete, get_char_files_from_dir
from language_handler import get_translation
from utils import get_moves as get_moves_json_array, get_key_and_content_from_message, get_args_from_content, format_labels, validate_labels, get_folder_from_message, get_key_from_ctx, get_key_and_content_from_ctx, format_labels_changed, get_channel_from_ctx
from constants import  LABELS, VALUE, LOCKED, POTENTIAL, PENDING_ADVANCEMENTS, CONDITIONS, MOVES, ADVANCEMENT, MAX_LABEL_VALUE, MIN_LABEL_VALUE, PLAYBOOK_INTERACTIONS, DESCRIPTION, TAKEN

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


def format_conditions(conditions, lang):
    if not len(conditions):
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.condition_not_marked')

    response = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.youre')

    for condition in conditions:
        if conditions[condition]:
            response = response + f"  - {get_translation(lang, f'conditions.{condition}')}\n"

    return response

def format_conditions_slash(conditions, lang, condition, what):
    if not len(conditions):
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.condition_not_marked')
    if what == 'mark':
        response = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.marked')
    elif what == 'clear':
        response = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.cleared')
    response = response + f"{get_translation(lang, f'conditions.{condition}')}\n"
    response = response + get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.youre')

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

def invert_condition_slash(ctx, lang, condition, what):
    key = get_key_from_ctx(ctx)
    condition_name_og = condition
    condition_name = get_translation(lang, f'inverted_conditions.{condition_name_og}')

    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    conditions = char_info[CONDITIONS]

    if condition_name not in conditions:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.invalid_condition')

    condition_to_mark = conditions[condition_name]

    if conditions[condition] == False:
        conditions[condition] = True
    elif conditions[condition] == True:
        conditions[condition] = False

    #if condition_to_mark == compare_to:
        #return get_condition_is_unchangable(compare_to, lang)

    #char_info[CONDITIONS][condition_name] = compare_to

    upload_to_s3(char_info, key, s3_client)

    return format_conditions_slash(char_info[CONDITIONS], lang, condition, what)



def format_moves(moves):
    return ''


def format_advance_list(advance_list, list_name, lang):
    response = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.{list_name}') + '\n'

    for advance_key in advance_list:
        advance = advance_list[advance_key]
        description = advance[DESCRIPTION]
        response = response + '• '
        if advance[TAKEN]:
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

    labels_do_not_exist = validate_labels(lang, [label_to_increase_name_og, label_to_decrease_name_og])
    if labels_do_not_exist:
        return labels_do_not_exist

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

def edit_labels_slash(ctx, lang, labelup, labeldown):
    key = get_key_from_ctx(ctx)
    label_to_increase_name_og = labelup
    label_to_decrease_name_og = labeldown

    if label_to_increase_name_og == label_to_decrease_name_og:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.different_labels')

    label_to_increase_name = get_translation(lang, f'inverted_labels.{label_to_increase_name_og}')
    label_to_decrease_name = get_translation(lang, f'inverted_labels.{label_to_decrease_name_og}')

    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    labels = char_info[LABELS]

    labels_do_not_exist = validate_labels(lang, [label_to_increase_name_og, label_to_decrease_name_og])
    if labels_do_not_exist:
        return labels_do_not_exist

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

    return format_labels_changed(labels, lang, label_to_increase_name, label_to_decrease_name)

def lock_label(message, lang):
    key, content = get_key_and_content_from_message(message)
    label_to_lock_name_og = get_args_from_content(content)
    label_to_lock_name = get_translation(lang, f'inverted_labels.{label_to_lock_name_og}')

    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    labels = char_info[LABELS]

    label_does_not_exist = validate_labels(lang, [label_to_lock_name_og])
    if label_does_not_exist:
        return label_does_not_exist

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
        potential = 0
        upload_to_s3(char_info, key, s3_client)
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.congrats_pending_advancements')(char_info[PENDING_ADVANCEMENTS])

    potential = potential + 1
    char_info[POTENTIAL] = potential

    upload_to_s3(char_info, key, s3_client)
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.congrats_potential')(potential)

def remove_potential(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    potential = char_info[POTENTIAL]
    if potential > 0:
        potential = potential - 1
        char_info[POTENTIAL] = potential
        upload_to_s3(char_info, key, s3_client)
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.congrats_potential')(potential)
    elif potential == 0:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.nopotential')



def mark_condition(message, lang):
    return invert_condition(message, True, lang)


def condition_slash(ctx, lang, condition, what):
    return invert_condition_slash(ctx, lang, condition, what)


def clear_condition(message, lang):
    return invert_condition(message, False, lang)

# def clear_condition_slash(ctx, lang,condition):
#     return invert_condition_slash(ctx, False, lang, condition)


def replicate_character(ctx, lang, channel_id):
    key, content = get_key_and_content_from_ctx(ctx)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.existing_character')
    link_server = channel_id
    file_list = get_files_from_dir('playbooks', s3_client)
    template_key = f'playbooks/blank'
    matching_files = list(filter(lambda file_info: file_info["Key"] == f'{template_key}.json', file_list["Contents"]))
    template = info_from_s3(template_key, s3_client)
    upload_to_s3(template, key, s3_client)
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.character_replication')(character_name, formated_playbook_name)

def create_character(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()

    char_info = info_from_s3(key, s3_client)
    if char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.existing_character')

    playbook_name, character_name, player_name, label_to_increase_og = get_args_from_content(content)

    label_does_not_exist = validate_labels(lang, [label_to_increase_og])
    if label_does_not_exist:
        return label_does_not_exist

    label_to_increase = get_translation(lang, f'inverted_labels.{label_to_increase_og}')
    translated_name = get_translation(lang, f'playbooks.names.{playbook_name}')
    file_list = get_files_from_dir('playbooks', s3_client)
    template_key = f'playbooks/{translated_name}'

    matching_files = list(filter(lambda file_info: file_info["Key"] == f'{template_key}.json', file_list["Contents"]))

    if not matching_files:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_template')(playbook_name)

    template = info_from_s3(template_key, s3_client)

    template[LABELS][label_to_increase][VALUE] = template[LABELS][label_to_increase][VALUE] + 1
    template['characterName'] = character_name
    template['playerName'] = player_name

    upload_to_s3(template, key, s3_client)

    formated_playbook_name = playbook_name.capitalize()
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.congrats_on_creation')(character_name, formated_playbook_name)

def create_character_slash(ctx, lang, playbook_name, character_name, player_name, label_to_increase_og):
    key = get_key_from_ctx(ctx)
    s3_client = get_s3_client()

    char_info = info_from_s3(key, s3_client)
    if char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.existing_character')

    label_does_not_exist = validate_labels(lang, [label_to_increase_og])
    if label_does_not_exist:
        return label_does_not_exist

    label_to_increase = get_translation(lang, f'inverted_labels.{label_to_increase_og}')
    translated_name = get_translation(lang, f'playbooks.names.{playbook_name}')
    file_list = get_files_from_dir('playbooks', s3_client)
    template_key = f'playbooks/{translated_name}'

    matching_files = list(filter(lambda file_info: file_info["Key"] == f'{template_key}.json', file_list["Contents"]))

    if not matching_files:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_template')(playbook_name)

    template = info_from_s3(template_key, s3_client)

    template[LABELS][label_to_increase][VALUE] = template[LABELS][label_to_increase][VALUE] + 1
    template['characterName'] = character_name
    template['playerName'] = player_name

    upload_to_s3(template, key, s3_client)

    formated_playbook_name = playbook_name.capitalize()
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.congrats_on_creation')(character_name, formated_playbook_name)

def delete_character(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if char_info:
        character_name = char_info['characterName']
        formated_playbook_name = char_info['playbook'].capitalize()
        s3_delete(key, s3_client)
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.character_deletion')(character_name, formated_playbook_name)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

def delete_character_ctx(ctx, lang):
    key = get_key_from_ctx(ctx)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if char_info:
        character_name = char_info['characterName']
        formated_playbook_name = char_info['playbook'].capitalize()
        s3_delete(key, s3_client)
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.character_deletion')(character_name, formated_playbook_name)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')


# These are the functions that get the data in the characters s3 file

def get_character(message):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    return info_from_s3(key, s3_client)

def get_character_ctx(ctx):
    key = get_key_and_content_from_ctx(ctx)
    s3_client = get_s3_client()
    return info_from_s3(key, s3_client)


#def get_all_characters(message):
#    key, _content = get_folder_from_message(message)
#    s3_client = get_s3_client()
#    return info_from_s3(key, s3_client)

def get_labels(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    return format_labels(char_info[LABELS], lang)


def get_labels_slash(ctx, lang):
    key = get_key_from_ctx(ctx)
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


def get_conditions_slash(ctx, lang):
    key = get_key_from_ctx(ctx)
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

    return get_translation(lang,  f'{PLAYBOOK_INTERACTIONS}.potential')(potential)


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

def get_sheet(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    return char  #format_advancements(char_info[C], lang)

def print_playbook(message, lang):
    key, _content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')
    char_text = f'You are {char_info["characterName"]}, a {char_info["playbook"].capitalize()}.'
    #this case handles if the character is a replica
    if char_info.get('replicate_key'):
#        repl_id = char_info.get('replicate_key').split('/')[1]
#        this_id = message.channel.get("id")
        char_text = f'You are a copy of {char_info["characterName"]}, a {char_info["playbook"].capitalize()}.'
    return char_text

def print_playbook_slash(ctx, lang):
    key = get_key_from_ctx(ctx)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')
    char_text = f'You are {char_info["characterName"]}, a {char_info["playbook"].capitalize()}.'
    #this case handles if the character is a replica
    if char_info.get('replicate_key'):
#        repl_id = char_info.get('replicate_key').split('/')[1]
#        this_id = message.channel.get("id")
        char_text = f'You are a copy of {char_info["characterName"]}, a {char_info["playbook"].capitalize()}.'
    return char_text

def print_party(ctx,lang):
    key = get_channel_from_ctx(ctx)
    s3_client = get_s3_client()
    party = get_char_files_from_dir(key,s3_client)
    response = "The Party is made up of:\n"
    for player in party:
        if 'settings' not in player: #here we need to ignore settings.json files :D
            player_key = player.split('.')[0]
            char_info = info_from_s3(player_key, s3_client)
            response = response + f' - {char_info["characterName"]} the {char_info["playbook"].capitalize()} played by {char_info["playerName"]}\n'

    return response

def get_influence(ctx, lang):
    import os
    s3_client = get_s3_client()
    channel_key = get_channel_from_ctx(ctx)
    party = get_char_files_from_dir(channel_key, s3_client)

    char_key = get_key_from_ctx(ctx)
    char_info = info_from_s3(char_key, s3_client)
    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    #What if they've never checked influence before - add an empty array
    if 'influenceOver' not in char_info:
        char_info['influenceOver'] = []
        #upload_to_s3(char_info, char_key, s3_client)
        party_list = [file for file in list(party) if os.path.basename(file) != "settings.json"]
        if len(party_list) <= 1:
            return 'No other players in the party.'
        for player in party:
            if 'settings' not in player:  # here we need to ignore settings.json files :D
                player_key = player.split('.')[0]
                party_info = info_from_s3(player_key, s3_client)

                if party_info['characterName'] != char_info['characterName']:
                    char_info['influenceOver'].append({'id': party_info['characterName'], 'hasInfluence': False})
        upload_to_s3(char_info, char_key, s3_client)
    #However if they do have influence make sure the whole party is in the array!
    elif 'influenceOver' in char_info:
        party_list = [file for file in list(party) if os.path.basename(file) != "settings.json"]
        if len(party_list) <= 1:
            return 'No other players in the party.'
        existing_character_names = [influence['id'] for influence in char_info['influenceOver']]
        for player in party_list:
            if 'settings' not in player:  # here we need to ignore settings.json files :D
                player_key = player.split('.')[0]
                party_info = info_from_s3(player_key, s3_client)

                if party_info['characterName'] != char_info['characterName'] and party_info['characterName'] not in existing_character_names:
                    char_info['influenceOver'].append({'id': party_info['characterName'], 'hasInfluence': False})
        upload_to_s3(char_info, char_key, s3_client)

    response = char_info
    return response


def invert_influence(ctx, character_name, char_info):
    # Find the character in the influenceOver array and toggle its influence status
    for char in char_info['influenceOver']:
        if char['id'] == character_name:
            char['hasInfluence'] = not char['hasInfluence']
            break

    # Update the character info in S3
    s3_client = get_s3_client()
    char_key = get_key_from_ctx(ctx)
    upload_to_s3(char_info, char_key, s3_client)

generic_playbook_dict = {
  "lock": lock_label,
  "editlabels": edit_labels,
  "potential": mark_potential,
  "removepotential": remove_potential,
  "markcondition": mark_condition,
  "clearcondition": clear_condition,
  "create": create_character,
  "labels": get_labels, 
  "conditions": get_conditions, 
  "get_potential": get_potential, 
  "pending_advancements": get_pending_advancements, 
  "advancements": get_advancements,
  "me": get_sheet,
  "print": print_playbook,
  "deletecharacter": delete_character,
    "replicate": replicate_character,
  "el": edit_labels,
  "cc": clear_condition,
  "mc": mark_condition
}

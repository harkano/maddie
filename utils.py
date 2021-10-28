import json
from language_handler import get_translation
from constants import MAX_POSITIVE_MOD, MIN_NEGATIVE_MOD, SUM, SUB, PLAYBOOK_INTERACTIONS, VALUE, LOCKED

def get_modified_num(mod, num):
    if mod == SUM: return min(num, MAX_POSITIVE_MOD)
    if mod == SUB: return -1 * min(num, MIN_NEGATIVE_MOD)
    return num

def get_modified_num_ctx(modifier):
    if modifier >= MAX_POSITIVE_MOD: return MAX_POSITIVE_MOD
    if modifier <= -1 * MIN_NEGATIVE_MOD: return -1 * MIN_NEGATIVE_MOD
    return modifier


def get_cap(num):
    if num >= MAX_POSITIVE_MOD:
        return MAX_POSITIVE_MOD
    if num <= (-1 * MIN_NEGATIVE_MOD):
        return (-1 * MIN_NEGATIVE_MOD)
    return num

def get_cap_ctx(num):
    if num >= MAX_POSITIVE_MOD:
        return MAX_POSITIVE_MOD
    if num <= -1 * MIN_NEGATIVE_MOD:
        return -1 * MIN_NEGATIVE_MOD
    return num

def get_moves(language = 'en'):
    ##Load in the existing moves
    input_file = open (f'language_files/{language}.json', encoding='utf-8')
    json_array = json.load(input_file)

    return json_array


def get_key_and_content_from_message(message):
    key = f'{message.channel.id}/{message.author.id}'

    return f'adventures/{key}', message.content

def get_key_from_ctx(ctx):
    key = f'{ctx.channel_id}/{ctx.author.id}'
    return f'adventures/{key}'

def get_key_and_content_from_ctx(ctx):
    key = f'{ctx.channel_id}/{ctx.author.id}'
    return f'adventures/{key}'

def get_replicate_key_and_content_from_message(message):
    link_channel = get_args_from_content(message.content)
    key = f'{link_channel}/{message.author.id}'

    return f'adventures/{key}', message.content


def get_folder_from_message(message):
    key = f'{message.channel.id}/'
    return f'adventures/{key}', message.content

def get_args_from_content(content):
    from tssplit import tssplit
    #splited = content.split(" ")
    splited = tssplit(content, quote='"', delimiter=' ')
    if len(splited) == 2:
        return splited[1]

    return splited[1:]


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


def format_labels_changed(labels, lang, labelup, labeldown):
    response = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.labels_change')(labelup.capitalize(), labeldown.capitalize())
    response = response + get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.labels_base')

    for label in labels:
        name = get_translation(lang, f'labels.{label}').capitalize()
        value = labels[label][VALUE]

        if labels[label][LOCKED]:
            is_locked = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.locked')
        else:
            is_locked = ''

        response = response + f'{name}: {value} {is_locked}\n'

    return response

def validate_labels(lang, inputed_labels):
    result = ''
    labels = get_translation(lang, f'inverted_labels')

    for label in inputed_labels:
        if label not in labels:
            result += get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.invalid_label')(label)

    return result


def format_flares(lang, flares):
    response = get_translation(lang, 'playbooks.nova.yourFlares')
    for flare in flares:
        if flare:
            translated_flare = get_translation(lang, f'playbooks.nova.names.{flare}').capitalize()
            response += f'\n• {translated_flare}'


def get_move(move, language = 'en'):
    ##Load in the existing moves
    input_file = open (f'language_files/{language}.json', encoding='utf-8')
    json_array = json.load(input_file)
    move_data = json_array['moves'][move]
    return move_data
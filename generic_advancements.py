# Missing advs
#   "loseInfluence": ,
#   "mot": ,
#   "motAgain": ,
#   "retire": ,
#   "playbookChange": ,

from utils import get_moves as get_moves_json_array, get_key_and_content_from_message, get_args_from_content, format_labels, validate_labels
from s3_utils import info_from_s3, get_s3_client, upload_to_s3
from language_handler import get_translation
from constants import PLAYBOOK_INTERACTIONS, MOVES, PENDING_ADVANCEMENTS, PICKED, SHORT_NAME, SPECIAL, ID, PLAYBOOK, LABELS, VALUE, MAX_LABEL_VALUE, MIN_LABEL_VALUE

def add_move_from_your_playbook(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)

    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')

    move_name = get_args_from_content(content)

    moves_array = get_moves_json_array(lang)[MOVES]
    move_list = list(filter(lambda move_dict: move_dict[SHORT_NAME] == move_name and not move_dict[SPECIAL], moves_array))

    if not len(move_list):
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_moves_pb')

    id = move_list[0][ID]

    move = list(filter(lambda dic: dic[ID] == id, char_info[MOVES]))[0]

    if move[PICKED]:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.move_already_taken')

    char_info[PENDING_ADVANCEMENTS] = char_info[PENDING_ADVANCEMENTS] - 1
    move[PICKED] = True
    upload_to_s3(char_info, key, s3_client)

    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.successfully_added_move')(move_name)


def add_moves(char_info, lang, move_name, s3_client, json_lang = 'en'):
    moves_array = get_moves_json_array(json_lang)[MOVES]
    move_list = list(filter(lambda move_dict: move_dict[SHORT_NAME] == move_name, moves_array))

    if not len(move_list):
        return False, get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_moves_pb')

    move = move_list[0]

    if move[PLAYBOOK] == char_info[PLAYBOOK]:
        return False, get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.your_playbook')

    id = move_list[0][ID]

    move = list(filter(lambda dic: dic[ID] == id, char_info[MOVES]))

    if len(move):
        return False, get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.move_already_taken')

    char_info[PENDING_ADVANCEMENTS] = char_info[PENDING_ADVANCEMENTS] - 1
    char_info[MOVES].append({ "id": id, "picked": True })

    return True, get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.successfully_added_move')(move_name)


def add_move_from_other_playbook(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)

    if not char_info:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_character')
    move_name = get_args_from_content(content)
    success, response = add_moves(char_info, lang, move_name, s3_client, lang)

    if success:
        upload_to_s3(char_info, key, s3_client)

    return response


def rearrange_labels(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    new_label_values = get_args_from_content(content)
    labels = char_info[LABELS]

    total_sum = 0
    new_sum = 0

    labels_do_not_exist = validate_labels(lang, labels)
    if labels_do_not_exist:
        return labels_do_not_exist

    for value in new_label_values:
        int_value = int(value)

        if int_value < MIN_LABEL_VALUE:
            return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.less_than_min')(MIN_LABEL_VALUE, int_value)

        if int_value > MAX_LABEL_VALUE:
            return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.greater_than_max')(MAX_LABEL_VALUE, int_value)

        new_sum = new_sum + int_value

    for label in labels:
        total_sum = total_sum + int(labels[label][VALUE])

    if total_sum + 1 != new_sum:
        difference = abs(new_sum - total_sum)
        if new_sum - total_sum > 0:
            direction = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.more')
        elif total_sum == new_sum:
            difference = ''
            direction = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.equal')
        else:
            direction = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.less')

        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.add_one_to_label')(difference, direction)

    index = 0
    for label in labels:
        labels[label][VALUE] = int(new_label_values[index])
        index += 1

    upload_to_s3(char_info, key, s3_client)
    return format_labels(labels, lang)


generic_advancements_dict = {
  "mov_my_playbook": add_move_from_your_playbook,
  "mov_other_playbook": add_move_from_other_playbook,
  "rearrange": rearrange_labels
}

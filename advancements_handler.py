# Missing advs
#   "confront": ,
#   "paragon": ,
#   "powers": ,
#   "abilities": ,
#   "doom": ,
#   "mutate": ,
#   "lockLessons": ,
#   "pastParagon": ,
#   "joinAbilities": ,
#   "advance": ,
#   "shame": ,
#   "enhancement": ,
#   "noAegis": ,
#   "civilian": ,
#   "future": ,
#   "depart": ,

from utils import get_moves as get_moves_json_array, get_key_and_content_from_message, get_args_from_content, format_labels, validate_labels, format_flares
from s3_utils import info_from_s3, get_s3_client, upload_to_s3, get_files_from_dir
from language_handler import get_translation
from constants import PLAYBOOK_INTERACTIONS, MOVES, PENDING_ADVANCEMENTS, SHORT_NAME, ID, PLAYBOOK, LABELS, VALUE, MAX_LABEL_VALUE, HEART, BULL, ROLES, ADULT, DELINQUENT, DOOMED, DOOMSIGNS, NOVA, FLARES, JANUS, MASK_LABEL, BEACON, DRIVES, DRIVES_DESCRIPTION, LEGACY, SANCTUARY, OUTSIDER, SECRET_IDENTITY, PROTEGE, RESOURCES, MAX_RESOURCES_TO_ADD, MENTOR, SOLDIER, INNOCENT, INNOCENT, NEWBORN, REFORMED, LOCKED, SCION, STAR
from generic_advancements import add_moves


def get_more_bull_roles(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)

    if char_info[PLAYBOOK] != BULL:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_playbook')(get_translation(lang, f'playbooks.inverted_names.{BULL}'))

    new_roles = get_args_from_content(content)
    already_picked = ''
    acum = ''
    roles = char_info[HEART][ROLES]
    translated_roles = []

    for role in new_roles:
        translated_role = get_translation(lang, f'playbooks.bull.roles.titles_dict')[role]
        translated_roles.append(translated_role)

        if translated_role not in roles:
            acum += f'\n• {role}'
        elif roles[translated_role]:
            already_picked = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.role_is_picked')(role)


    if len(acum):
        return already_picked + '\n' + get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.invalid_roles') + acum
    if already_picked:
        return already_picked

    for translated_role in translated_roles:
        roles[translated_role] = True

    upload_to_s3(char_info, key, s3_client)
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.successfull_update')


def add_one_to_two_labels(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)

    if char_info[PLAYBOOK] != DELINQUENT:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_playbook')(get_translation(lang, f'playbooks.inverted_names.{DELINQUENT}'))

    labels_to_upgrade = get_args_from_content(content)
    labels = char_info[LABELS]

    labels_do_not_exist = validate_labels(lang, labels_to_upgrade)
    if labels_do_not_exist:
        return labels_do_not_exist

    for label_name in labels_to_upgrade:
        label_to_increase = get_translation(lang, f'inverted_labels.{label_name}')
        value = int(labels[label_to_increase][VALUE])

        if value == MAX_LABEL_VALUE:
            return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.already_max')(value, label_name)

        labels[label_to_increase][VALUE] = 1 + value

    upload_to_s3(char_info, key, s3_client)
    return format_labels(labels, lang)


def clear_doomsign(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)

    if char_info[PLAYBOOK] != DOOMED:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_playbook')(get_translation(lang, f'playbooks.inverted_names.{DOOMED}'))

    doomsign_og = get_args_from_content(content)

    doomsign = get_translation(lang, f'playbooks.doomed.doomsigns.accessors.{doomsign_og}')
    if not doomsign:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.invalid_doomsign')(doomsign_og)

    char_doomsign = char_info[DOOMSIGNS][doomsign]
    if not char_doomsign:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.doomsign_not_marked')(doomsign_og)

    char_doomsign = True
    upload_to_s3(char_info, key, s3_client)
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.successfull_update')


def change_mask_label(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    new_mask_label_og = get_args_from_content(content)

    if char_info[PLAYBOOK] != JANUS:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_playbook')(get_translation(lang, f'playbooks.inverted_names.{JANUS}'))

    label_does_not_exist = validate_labels(lang, [new_mask_label_og])
    if label_does_not_exist:
        return label_does_not_exist

    new_mask_label = get_translation(lang, f'inverted_labels.{new_mask_label_og}')

    if new_mask_label == char_info[MASK_LABEL]:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.already_mask_label')(new_mask_label_og)

    new_label_value = char_info[LABELS][new_mask_label][VALUE]

    if new_label_value == MAX_LABEL_VALUE:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.already_max')(new_label_value, new_mask_label_og)

    char_info[LABELS][new_mask_label][VALUE] = new_label_value + 1
    char_info[MASK_LABEL] = new_mask_label
    upload_to_s3(char_info, key, s3_client)
    
    return format_labels(char_info[LABELS], lang)


def get_more_flares(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)

    if char_info[PLAYBOOK] != NOVA:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_playbook')(get_translation(lang, f'playbooks.inverted_names.{NOVA}'))

    new_flares = get_args_from_content(content)

    new_flares_count = len(new_flares)
    if new_flares_count != 3:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.not_exactly_three_flares')(new_flares_count)

    already_picked = ''
    acum = ''
    flares = char_info[FLARES]
    translated_flares = []

    for flare in new_flares:
        translated_flare = get_translation(lang, f'playbooks.nova.accessors.{flare}')
        translated_flares.append(translated_flare)

        if translated_flare not in flares:
            acum += f'\n• {flare}'
        elif flares[translated_flare]:
            already_picked = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.flare_is_picked')(flare)

    if acum:
        return already_picked + '\n' + get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.invalid_flares') + acum
    if already_picked:
        return already_picked

    for translated_flare in translated_flares:
        flares[translated_flare] = True

    upload_to_s3(char_info, key, s3_client)
    return format_flares(lang, flares)


def add_two_to_mentor_label(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)

    if char_info[PLAYBOOK] != PROTEGE:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_playbook')(get_translation(lang, f'playbooks.inverted_names.{PROTEGE}'))

    label_type_og = get_args_from_content(content)
    label_type = get_translation(lang, f'playbooks.protege.{label_type_og}')

    if not label_type:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.invalid_label_type')(label_type_og)

    label_name = char_info['mentor'][label_type]
    label_to_increase = char_info[LABELS][label_name]
    if label_to_increase[VALUE] > MAX_LABEL_VALUE - 1:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.max_mentor_label_value')(label_name, label_to_increase[VALUE])

    label_to_increase[VALUE] += 2

    upload_to_s3(char_info, key, s3_client)
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.successfull_update')


def get_invaild_resource_response(lang, resource, current_resources):
    response = get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.invalid_resource')(resource)
    valid_resources = get_translation(lang, f'playbooks.protege.resources_accessors')
    descriptions = get_translation(lang, f'playbooks.protege.resources')

    for resource in valid_resources:
        resource_name = valid_resources[resource]
        resource_description = descriptions[resource_name]

        if not current_resources[resource_name]:
            response += f'\n• {resource} ({resource_description})'

    return response    


def add_resources(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)

    if char_info[PLAYBOOK] != PROTEGE:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_playbook')(get_translation(lang, f'playbooks.inverted_names.{PROTEGE}'))

    resources_og = get_args_from_content(content)

    resources_count = len(resources_og)
    if resources_count > MAX_RESOURCES_TO_ADD:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.more_than_four_resources')(MAX_RESOURCES_TO_ADD, resources_count)

    current_resources = char_info[MENTOR][RESOURCES]
    resource_count = 0
    resources = []
    already_acquired = []

    for resource_og in resources_og:
        resource = get_translation(lang, f'playbooks.protege.resources_accessors.{resource_og}')
        if not resource:
            return get_invaild_resource_response(lang, resource_og, current_resources)

        if current_resources[resource]:
            already_acquired.append(resource_og)
        else:
            resources.append(resource)

    if already_acquired:
        response =  get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.resource_already_acquired')
        
        for resource in already_acquired:
            response += f'\n• {resource}'

        return response

    for resource in resources:
        current_resources[resource] = True

    upload_to_s3(char_info, key, s3_client)
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.successfull_update')


def lock_soldier(message, lang):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)

    if char_info[PLAYBOOK] != SOLDIER:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_playbook')(get_translation(lang, f'playbooks.inverted_names.{SOLDIER}'))

    soldier = char_info[LABELS][SOLDIER]
    if soldier[LOCKED]:
        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.already_locked')(get_translation(lang, f'playbooks.inverted_names.{SOLDIER}'))

    soldier[LOCKED] = True

    return format_labels(labels, lang)


# Here are the take X from Y playbook advances
# Example: _take sanctuary from the doomed playbook_

def get_legacy(message, lang):
    return get_part_of_playbook(message, lang, LEGACY, [STAR], [LEGACY], [LEGACY], f'playbooks.inverted_names.{LEGACY}')


def get_mentor(message, lang):
    return get_part_of_playbook(message, lang, PROTEGE, [INNOCENT], [MENTOR], [], 'playbooks.protege.mentor.title')


def get_secret_identity(message, lang):
    return get_part_of_playbook(message, lang, JANUS, [OUTSIDER, SCION], [MASK_LABEL, SECRET_IDENTITY], ['obligations'], 'playbooks.janus.title')


def get_heart(message, lang):
    return get_part_of_playbook(message, lang, BULL, [NOVA], [HEART], [], 'playbooks.bull.title')


def get_sanctuary(message, lang):
    return get_part_of_playbook(message, lang, DOOMED, [LEGACY], [SANCTUARY], [], 'playbooks.doomed.sanctuary.title')


def get_drives(message, lang):
    return get_part_of_playbook(message, lang, BEACON, [JANUS, REFORMED], [DRIVES, DRIVES_DESCRIPTION], [], 'playbooks.beacon.drives')


def get_burns(message, lang):
    return get_part_of_playbook(message, lang, NOVA, [DOOMED, NEWBORN], [FLARES], ['chargeburn'], 'playbooks.nova.flares')


def get_part_of_playbook(message, lang, playbook_to_take_from, your_playbook_must_be, what_to_take, moves, cant_take_message):
    key, content = get_key_and_content_from_message(message)
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)

    if char_info[PLAYBOOK] not in your_playbook_must_be:
        allowed_playbooks = ''
        for playbook in your_playbook_must_be:
            translated_playbook = get_translation(lang, f'playbooks.inverted_names.{playbook}')
            allowed_playbooks += f'\n• {translated_playbook}'

        return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.no_playbook')(allowed_playbooks)

    playbook_template = info_from_s3(f'playbooks/{playbook_to_take_from}', s3_client)

    for take_this in what_to_take:
        if take_this in char_info:
            return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.already_have')(get_translation(lang, cant_take_message))

        char_info[take_this] = playbook_template[take_this]

    for move in moves:
        success, response = add_moves(char_info, lang, move, s3_client)

        if not success:
            return response

    upload_to_s3(char_info, key, s3_client)
    return get_translation(lang, f'{PLAYBOOK_INTERACTIONS}.successfull_update')


playbook_specific_advancements_dict = {
  "more_roles": get_more_bull_roles,
  "more_to_labels": add_one_to_two_labels,
  "clear_sign": clear_doomsign,
  "get_burns": get_burns,
  "mask_label": change_mask_label,
  "get_drives": get_drives,
  "get_sanctuary": get_sanctuary,
  "more_flares": get_more_flares,
  "get_heart": get_heart,
  "get_mask": get_secret_identity,
  "mentor_label": add_two_to_mentor_label,
  "more_resources": add_resources,
  "get_mentor": get_mentor,
  "get_legacy": get_legacy,
  "lock_soldier": lock_soldier
}

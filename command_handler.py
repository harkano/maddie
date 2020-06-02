import logging
from playbook_interactions import lock_label, edit_labels, mark_potential, mark_condition, clear_condition, create_character, get_labels, get_conditions, get_potential, get_pending_advancements, get_advancements
from generic_advancements import add_move_from_your_playbook, add_move_from_other_playbook, rearrange_labels
from advancements_handler import get_more_bull_roles, add_adult_move, add_one_to_two_labels, clear_doomsign, get_burns, change_mask_label, get_drives, get_sanctuary, get_more_flares, get_heart, get_secret_identity, add_two_to_mentor_label, add_resources, get_mentor, get_legacy, lock_soldier
from config_interactions import get_settings, get_language, get_teamname, update_lang, update_gm, update_teamname, create_settings
from playbooks import get_moment_of_truth, get_playbooks
from language_handler import get_translation

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO) #set logging level to INFO, DEBUG if we want the full dump

def handle_help(message, _lang):
    log_line = message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
    logger.info(log_line)
    help_file = open("help", "r")
    response = help_file.read()
    return response


generic_playbook_dict = {
  "lock": lock_label,
  "editlabels": edit_labels,
  "potential": mark_potential,
  "markcondition": mark_condition,
  "clearcondition": clear_condition,
  "create": create_character,
  "labels": get_labels, 
  "conditions": get_conditions, 
  "get_potential": get_potential, 
  "pending_advancements": get_pending_advancements, 
  "advancements": get_advancements
}

settings_dict = {
  "helphere": handle_help,
  "settings": get_settings,
  "language": get_language,
  "teamname": get_teamname,
  "update_lang": update_lang,
  "update_gm": lambda msg, _lang: update_gm(msg),
  "update_teamname": lambda msg, _lang: update_teamname(msg),
  "create_settings": lambda msg, _lang: create_settings(msg)
}

generic_advancements_dict = {
  "mov_my_playbook": add_move_from_your_playbook,
  "mov_other_playbook": add_move_from_other_playbook,
  "rearrange": rearrange_labels
}

playbook_specific_advancements_dict = {
  "more_roles": get_more_bull_roles,
  "add_adult": add_adult_move,
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

embed_commands_dict = {
  "mot": get_moment_of_truth,
  "playbooks": lambda _msg, lang: get_playbooks(lang)
}

all_dicts = {
  "generic_playbook_dict": generic_playbook_dict,
  "settings_dict": settings_dict,
  "generic_advancements_dict": generic_advancements_dict,
  "playbook_specific_advancements_dict": playbook_specific_advancements_dict,
  "embed_commands_dict": embed_commands_dict
}


def plain_command_handler(message, lang):
    command = message.content.split(" ")[0][1:]
    for command_dict in all_dicts:
        translated_command = get_translation(lang, f'plain_commands.{command}')
        handler = all_dicts[command_dict].get(translated_command)

        if handler:
            return handler(message, lang)

    return ''


def plain_command_handler2(message, lang):
    command = message.content.split(" ")[0][1:]
    handler = plain_commands_dict.get(get_translation(lang, f'plain_commands.{command}'), lambda _msg, _lang: '')

    return handler(message, lang)


def embed_command_handler(message, lang):
    command = message.content.split(" ")[0][1:]

    handler = embed_commands_dict.get(get_translation(lang, f'embed_commands.{command}'), lambda _msg, _lang: '')

    return handler(message, lang)

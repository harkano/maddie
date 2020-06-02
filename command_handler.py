import logging
from playbook_interactions import generic_playbook_dict
from generic_advancements import generic_advancements_dict
from advancements_handler import playbook_specific_advancements_dict
from config_interactions import settings_dict
from playbooks import embed_commands_dict
from language_handler import get_translation

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO) #set logging level to INFO, DEBUG if we want the full dump

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
        translated_command = get_translation(lang, f'{command_dict}.{command}')
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

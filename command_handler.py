import logging
from playbook_interactions import generic_playbook_dict
from generic_advancements import generic_advancements_dict
from advancements_handler import playbook_specific_advancements_dict
from config_interactions import settings_dict, get_raw_lang
from playbooks import embed_commands_dict
from language_handler import get_translation, LANG_LIST

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO) #set logging level to INFO, DEBUG if we want the full dump

all_plain_dicts = {
  "generic_playbook_dict": generic_playbook_dict,
  "settings_dict": settings_dict,
  "generic_advancements_dict": generic_advancements_dict,
  "playbook_specific_advancements_dict": playbook_specific_advancements_dict
}


all_embed_dicts = {
  "embed_commands_dict": embed_commands_dict
}


def plain_command_handler(message):
    command = message.content.split(" ")[0][1:]
    for command_dict in all_plain_dicts:
        for lang in LANG_LIST:
          translated_command = get_translation(lang, f'{command_dict}.{command}')
          handler = all_plain_dicts[command_dict].get(translated_command)

          if handler:
              raw_lang = get_raw_lang(message)
              return handler(message, lang)

    return ''


def embed_command_handler(message):
    command = message.content.split(" ")[0][1:]
    for command_dict in all_embed_dicts:
        for lang in LANG_LIST:
          translated_command = get_translation(lang, f'{command_dict}.{command}')
          handler = all_embed_dicts[command_dict].get(translated_command)

          if handler:
              raw_lang = get_raw_lang(message)
              return handler(message, lang)

    return ''

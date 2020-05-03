import logging
from playbook_interactions import lock_label, edit_labels, mark_potential, mark_condition, clear_condition, create_character
from playbooks import get_moment_of_truth, get_playbooks
from language_handler import get_translation

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO) #set logging level to INFO, DEBUG if we want the full dump

def handle_help(message):
    log_line = message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
    logger.info(log_line)
    help_file = open("../../aws/help", "r")
    response = help_file.read()
    return response


plain_commands_dict = {
  "helphere": handle_help,
  "lock": lock_label,
  "editlabels": edit_labels,
  "potential": mark_potential,
  "markcondition": mark_condition,
  "clearcondition": clear_condition,
  "create": create_character
}


embed_commands_dict = {
  "mot": get_moment_of_truth,
  "playbooks": lambda msg: get_playbooks()
}

def plain_command_handler(message, lang):
    command = message.content.split(" ")[0][1:]

    handler = plain_commands_dict.get(get_translation(lang, f'plain_commands.{command}'), lambda msg: '')

    return handler(message)


def embed_command_handler(message, lang):
    command = message.content.split(" ")[0][1:]

    handler = embed_commands_dict.get(get_translation(lang, f'embed_commands.{command}'), lambda msg: '')

    return handler(message)

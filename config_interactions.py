# import boto3 # This is unused in this file.
import json
from storage import info_from_s3, get_s3_client, upload_to_s3, get_files_from_dir, s3_delete
from language_handler import get_translation, get_for_all_langs, is_invalid_lang
from constants import CONFIGURATION

LANGUAGE = 'language'
GM = 'gm'
TEAMNAME = 'teamname'
CUSTOM_NAMES = 'customNames'
TEAM = 'team'
DICEDISPLAY = 'dicedisplay'

# Aux functions

def no_config_file():
    return get_for_all_langs('configuration.no_file')


def get_settings_path(message):
    return f'adventures/{message.channel.id}/settings'


def get_field_from_config(message, field):
    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)

    if not settings:
        return no_config_file()

    name = get_translation(settings[LANGUAGE], f'configuration.{field}').capitalize()

    return f'{name}: {settings[field]}'


def handle_help(message, _lang):
    #log_line = message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
    #logger.info(log_line)
    help_file = open("help", "r")
    response = help_file.read()
    return response


# Updaters

def generic_updater(message, field):
    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)

    if not settings:
        return no_config_file()

    from tssplit import tssplit
    new_value = tssplit(message.content, quote='"', delimiter=' ')[1]
    #new_value = message.content.split(" ")[1]
    settings[field] = new_value

    upload_to_s3(settings, settings_key, s3_client)

    return get_translation(settings[LANGUAGE], 'configuration.successfull_update')


def update_lang(message, lang):
    new_lang = message.content.split(" ")[1]

    if is_invalid_lang(new_lang):
        return get_translation(lang, 'configuration.invalid_lang')

    return generic_updater(message, LANGUAGE)


def update_gm(message):
    return generic_updater(message, GM)


def update_teamname(message):
    return generic_updater(message, TEAMNAME)


def create_settings(message):
    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)

    if settings:
        return get_translation(settings[LANGUAGE], 'configuration.existing_settings')

    lang = message.content.split(" ")[1]

    settings = {
        "language": lang,
        "gm": "",
        "teamname": "",
        "customNames": [],
        "team": 1,
        "dicedisplay": True

    }

    upload_to_s3(settings, f'adventures/{message.channel.id}/settings', s3_client)

    return get_translation(lang, 'configuration.successfull_creation')

def delete_settings(message):
    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)

    if not settings:
        return no_config_file()
    if settings:
        s3_delete(settings_key, s3_client)
        return get_translation(settings[LANGUAGE], 'configuration.successfull_deletion')

# Getters

def get_settings(message, _lang):
    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)

    if not settings:
        return no_config_file()

    response = get_translation(settings[LANGUAGE], 'configuration.settings')
    for field in settings:
        name = get_translation(settings[LANGUAGE], f'configuration.{field}')
        value = settings[field]
        response = response + f'{name}: {value}\n'

    return response


def get_raw_lang(message, _lang = None):
    try:
        settings_key = get_settings_path(message)
        s3_client = get_s3_client()
        settings = info_from_s3(settings_key, s3_client)

        if not settings:
            return 'en'

        return settings[LANGUAGE]
    except Exception as exception:
        return 'en'


def get_language(message, _lang):
    return get_field_from_config(message, LANGUAGE)


def get_teamname(message, _lang):
    return get_field_from_config(message, TEAMNAME)

#Team Pool Handling

def add_team(message, _lang, action):
    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)
    lang = settings[LANGUAGE]
    if not settings:
        return no_config_file()
    team = settings[TEAM]
    if action == 'increase':
        team = team + 1 #increment!
    elif action == 'decrease':
        if team > 0:
            team = team - 1 #spend!
        else: return get_translation(lang, 'configuration.insufficient_team')
    elif action == 'empty':
        team = 1
    settings[TEAM] = team #update team
    upload_to_s3(settings, settings_key, s3_client)
    response = get_translation(lang, f'{CONFIGURATION}.team_pool')(team)
    return response

def toggle_dice(message, _lang):
    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)
    lang = settings[LANGUAGE]
    if not settings:
        return no_config_file()
    dice = settings[DICEDISPLAY]
    if dice == True:
        dice = False
    elif dice == False:
        dice = True
    settings[DICEDISPLAY]=dice
    upload_to_s3(settings, settings_key, s3_client)
    response = get_translation(lang, f'{CONFIGURATION}.dicedisplayswitched')(dice)
    return response

def get_dicedisplay(message, _lang):

    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)
    if not settings:
        #return no_config_file()  ##need to fix this so it displays the message properly
        return True
    try:
        dicedisplay = settings[DICEDISPLAY]
    except:
        dicedisplay = True
    return dicedisplay

settings_dict = {
  "helphere": handle_help,
  "settings": get_settings,
  "language": get_language,
  "teamname": get_teamname,
  "update_lang": update_lang,
  "update_gm": lambda msg, _lang: update_gm(msg),
  "update_teamname": lambda msg, _lang: update_teamname(msg),
  "create_settings": lambda msg, _lang: create_settings(msg),
  "delete_settings": lambda msg, _lang: delete_settings(msg),
  "add_team": lambda msg, _lang: add_team(msg, _lang, 'increase'),
  "spend_team": lambda msg, _lang: add_team(msg, _lang, 'decrease'),
  "check_team": lambda msg, _lang: add_team(msg, _lang, 'check'),
  "empty_team": lambda msg, _lang: add_team(msg, _lang, 'empty'),
  "toggle_dice": lambda msg, _lang: toggle_dice(msg, _lang)
}

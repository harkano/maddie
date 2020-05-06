import boto3
import json
from s3_utils import info_from_s3, get_s3_client, upload_to_s3, get_files_from_dir
from language_handler import get_translation

LANGUAGE = 'language'
TEAMNAME = 'teamname'
CUSTOM_NAMES = 'customNames'

# Aux functions

def get_settings_path(message):
    return f'adventures/{message.channel.id}/settings'


def get_field_from_config(message, field):
    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)

    name = get_translation(settings[LANGUAGE], f'configuration.{field}').capitalize()

    return f'{name}: {settings[field]}'


# Updaters

def update_settings(key, language = '', gm = '', teamname = '', custom_names = ''):
    settings_key = f'adventures/{key}/settings'

    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)

    if language:
        settings[LANGUAGE] = language
    if teamname:
        settings[TEAMNAME] = teamname
    if custom_names:
        settings[CUSTOM_NAMES] = custom_names

    upload_to_s3(settings, settings_key, s3_client)


# Getters

def get_settings(message, _lang):
    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)

    response = get_translation(settings[LANGUAGE], 'configuration.settings')
    for field in settings:
        name = get_translation(settings[LANGUAGE], f'configuration.{field}')
        value = settings[field]
        response = response + f'{name}: {value}\n'

    return response


def get_raw_lang(message, _lang):
    settings_key = get_settings_path(message)
    s3_client = get_s3_client()
    settings = info_from_s3(settings_key, s3_client)

    return settings[LANGUAGE]


def get_language(message, _lang):
    return get_field_from_config(key, LANGUAGE)


def get_teamname(message, _lang):
    return get_field_from_config(key, TEAMNAME)

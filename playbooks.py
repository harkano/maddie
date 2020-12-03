import re
import discord
from utils import get_moves, get_key_and_content_from_message
from language_handler import get_translation
from s3_utils import info_from_s3, get_s3_client

def get_playbook_list(lang):
    return get_translation(lang, 'playbooks.list')


def format_playbook_name(name, lang):
    capitalized_name = name.capitalize()

    the = get_translation(lang, 'playbooks.the')
    return f'\n• {the} {capitalized_name}'


def get_playbook_names(lang):
    playbook_list = get_translation(lang, 'playbooks.list')
    return list(map(lambda name: format_playbook_name(name, lang), playbook_list))

def get_playbook_component(component, message, lang):
    key, _content = get_key_and_content_from_message(message)
    msg = message.content
    usr = message.author.display_name
    s3_client = get_s3_client()
    char_info = info_from_s3(key, s3_client)
    json_array = get_moves(lang)
    playbook_re = get_translation(lang, 'playbooks.playbook_re')
    #this case deals with if we have a character created, but waits to make sure they haven't passed a playbook in anyway
    result1 = re.search(playbook_re, msg)
    found = 0
    if result1 is not None:
        for p in json_array['playbooks']:
            if p['name'] == result1.group(1):
                mot = p['mot']
                cel = p['celebrate']
                wek = p['weakness']
                img = p['img']
                found = 1
    if found != 1:
        if char_info:
            playbook = char_info['playbook']
            charactername = char_info['characterName']
            for p in json_array['playbooks']:
                if p['name'] == playbook:
                    mot = p['mot']
                    cel = p['celebrate']
                    wek = p['weakness']
                    img = p['img']
                    user = charactername
                    found = 1
    if found == 1:
        description = get_translation(lang, 'description')
        if component == 'mot':
            embed = discord.Embed(title=get_translation(lang, 'playbooks.moment_of_truth'))
            embed.set_author(name=get_translation(lang, 'playbooks.this_is_mot')(usr))
            embed.add_field(name=description, value=mot)
        elif component == 'celebrate':
            embed = discord.Embed(title=get_translation(lang, 'playbooks.celebrate'))
            embed.set_author(name=get_translation(lang, 'playbooks.this_is_celebrate')(usr))
            embed.add_field(name=description, value=cel)
        elif component == 'weakness':
            embed = discord.Embed(title=get_translation(lang, 'playbooks.weakness'))
            embed.set_author(name=get_translation(lang, 'playbooks.this_is_weakness')(usr))
            embed.add_field(name=description, value=wek)
        embed.set_thumbnail(url=img)
        embed.set_footer(text=" ")
        response = embed
        return response
    else:
        response = 0

embed_commands_dict = {
  "mot": lambda msg, lang: get_playbook_component('mot', msg, lang),
  "playbooks": lambda _msg, lang: get_playbooks(lang),
  "celebrate": lambda msg, lang: get_playbook_component('celebrate', msg, lang),
  "weakness": lambda msg, lang: get_playbook_component('weakness', msg, lang)


}

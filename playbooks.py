import re
import discord
from utils import get_moves
from language_handler import get_translation

def get_playbook_list(lang):
    return get_translation(lang, 'playbooks.list')


def format_playbook_name(name, the, lang):
    capitalized_name = name.capitalize()

    the = get_translation(lang, 'playbooks.the')
    return f'\n• {the} {capitalized_name}'


def get_playbook_names(lang):
    playbook_list = get_translation(lang, 'playbooks.list')
    return list(map(format_playbook_name, playbook_list, lang))


def get_moment_of_truth(message, lang):
    msg = message.content
    usr = message.author.display_name
    json_array = get_moves(lang)
    found = 0
    msg = msg.lower()
    playbook_re = r'!mot ([a-z]+)'
    result1 = re.search(playbook_re, msg)
    for p in json_array['playbooks']:
        if p['name'] == result1.group(1):
            mot = p['mot']
            img = p['img']
            found = 1
    if found == 1:
        embed = discord.Embed(title=f"MOMENT OF TRUTH")
        embed.set_author(name=f"This is {usr}'s moment!")
        embed.set_thumbnail(url=img)
        description = get_translation(lang, 'description')
        embed.add_field(name=description, value=f"{mot}")
        embed.set_footer(text=" ")
        response = embed
    else: response = 0

    return response

def get_playbooks(lang):
    json_array = get_moves(lang)
    playbooks = get_translation(lang, 'playbooks.playbooks')
    embed = discord.Embed(title=playbooks)
    available = get_translation(lang, 'playbooks.available')
    embed.set_author(name=available)
    for s in json_array['sources']:
        line = ""
        for p in json_array['playbooks']:
            if s['source'] == p['source']:
                line = line + p['name'].capitalize() + ", "
        line = line.rstrip(', ')
        embed.add_field(name=f"{s['name']}", value=f"{line}", inline=False)
        embed.set_footer(text=" ")
        response = embed
    return response
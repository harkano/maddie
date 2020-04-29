PLAYBOOK_LIST = ['beacon', 'bull', 'delinquent', 'doomed', 'janus', 'legacy', 'nova', 'outsider', 'protege', 'transformed']

import re
import discord

def get_playbook_list ():
    return PLAYBOOK_LIST


def format_playbook_name (name):
    capitalized_name = name.capitalize()

    return f'\n• The {capitalized_name}'

def get_playbook_names ():
    return list(map(format_playbook_name, PLAYBOOK_LIST))

def get_moment_of_truth (msg,usr,json_array):
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
        embed.add_field(name="Description", value=f"{mot}")
        embed.set_footer(text=" ")
        response = embed
    else: response = 0

    return response

def get_playbooks (json_array):
    embed = discord.Embed(title=f"Playbooks")
    embed.set_author(name=f"Available Playbooks are - ")
    for s in json_array['sources']:
        line = ""
        for p in json_array['playbooks']:
            if s['source'] == p['source']:
                line = line + p['name'] + ", "
        line = line.rstrip(', ')
        embed.add_field(name=f"{s['name']}", value=f"{line}", inline=False)
        embed.set_footer(text=" ")
        response = embed
    return response
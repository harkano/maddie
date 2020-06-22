import re
import json
import discord
import random
import logging


from utils import get_modified_num, get_moves
from language_handler import get_translation
from config_interactions import get_raw_lang
from playbook_interactions import get_character
from constants import LABELS, CONDITIONS, VALUE


##Setup the big sub
def mad_parse(message):
    msg = message.content
    user = message.author.display_name
    blob = ""
    capital = ""
    phrase = ""
    word = ""
    mod = ""
    num = int(0)
    quiet = 0
    match = 0
    # parse command into parts
    msg = msg.lower()
    searchStr1 = r'[a-z]+'
    searchStr2 = r'[\+\-]'
    searchStr3 = r'[1234567890]'
    log_line = ''
    result1 = re.search(searchStr1, msg)
    if result1:
        log_line = log_line + result1.group(0)
        word = result1.group(0)
    else: log_line = log_line + "no cmd "
    result2 = re.search(searchStr2, msg)
    if result2:
        log_line = log_line + result2.group()
        mod = result2.group(0)
    else: log_line = log_line + "no mod "
    result3 = re.search(searchStr3, msg)
    if result3:
        log_line = log_line + result3.group(0)
        num = int(result3.group(0))
    else: log_line = log_line + "no num "

    lang = get_raw_lang(message)
    json_array = get_moves(lang)

 # figure out which type of modifier it is#
 # lookup a table for the big blob of text and a wee blob#
    for p in json_array['moves']:
        if p['shortName'] == word:
            blob = p['blob']
            capital = p['capital']
            phrase = p['phrase']
            img = p['img']
            roll = p['requiresRolling']
            label = p['label']
            condition = p.get('condition', '')
            match = 1
    #Quiet mode
    searchStr4 = r'!!'
    result4 = re.search(searchStr4, msg)
    if result4: quiet = 1

    #Ugly format blob!#
    if match == 1 : #lets us ignore ! prefix commands that aren't in our list
        embed=discord.Embed(title=f"{capital}")
        embed.set_author(name=f"{user} {phrase}")
        embed.set_thumbnail(url=img)
        desc = get_translation(lang, 'description')
        if quiet == 0: embed.add_field(name=desc, value=f"{blob}") # don't include the blob if we're in quiet mode (!!)
        if roll:
            handle_roll(message, embed, num, mod, lang, label, condition)
        embed.set_footer(text=" ")

        return embed

    else:
        return 0


def get_modifier_from_character(labels, conditions, label, condition):
    mod = 0

    if condition and conditions[condition]:
        mod = -2

    if label == CONDITIONS:
        conditions_count = 0
        for condition in conditions:
            if conditions[condition]:
                conditions_count += 1

        return mod + conditions_count

    if label not in ['adult', 'basic']:
        mod += labels[label][VALUE]

    return mod


def handle_roll(message, embed, num, mod, lang, label, condition):
    character = get_character(message)

    char_mod = 0
    if character:
        char_mod = get_modifier_from_character(character[LABELS], character[CONDITIONS], label, condition)

    num_calc = get_modified_num(mod, num + char_mod)

    add_result(embed, num_calc, mod, lang)


def add_result (embed, num_calc, mod, lang):
    #do dice rolling
    result1 = random.randrange(1,7) ##first d6
    result2 = random.randrange(1,7) ##second d6
    result_tot = result1 + result2 + num_calc

    if mod == '-':
        modifier_to_show = ''
    else:
        modifier_to_show = f' {mod}'

    calculation_title = get_translation(lang, 'dice_rolling.calculation_title')
    calculation = get_translation(lang, 'dice_rolling.calculation')(result1, result2, modifier_to_show, num_calc)
    result = get_translation(lang, 'dice_rolling.result')

    embed.add_field(name=calculation_title, value=calculation, inline=False)
    embed.add_field(name=result, value=f"**{result_tot}**")

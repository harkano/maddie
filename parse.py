import re
import discord
import random
import logging

from utils import get_modified_num, get_moves, get_cap, get_move, get_modified_num_ctx, get_cap_ctx
from language_handler import get_translation
from config_interactions import get_raw_lang, get_dicedisplay
from playbook_interactions import get_character, get_character_ctx
from constants import LABELS, CONDITIONS, VALUE, dice, modifier_emojis

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
    if "?" in msg:
        roll = False
        quiet = 0
    #Find out if user has dicedisplay set to false
    dicedisplay = True
    dicedisplay = get_dicedisplay(message, lang)

    #Ugly format blob!#
    if match == 1 : #lets us ignore ! prefix commands that aren't in our list
        character = get_character(message)
        embed=discord.Embed(title=f"{capital}", colour=5450873)
        embed.set_footer(text=" ")
        embed.set_author(name=f"{user} {phrase}")
        #embed.set_author(name=f"{user} {phrase}")
        embed.set_thumbnail(url=img)
        desc = get_translation(lang, 'description')
        if quiet == 0: embed.add_field(name=desc, value=f"{blob}") # don't include the blob if we're in quiet mode (!!)
        addendum = None
        if roll:
            addendum = handle_roll(character, message, embed, num, mod, lang, label, condition, user)
#        embed.set_footer(text=" ")
#       embed.set_author(name=f"{user} {phrase}")
        if dicedisplay:
            return (embed, addendum)
        return (embed, '')

    else:
        return None


def slash_parse(ctx, move, modifier=0):
    move_data = get_move(move)
    character = get_character_ctx(ctx)
    embed=discord.Embed(title=f"{move_data['capital']}", colour=5450873)
    embed.set_footer(text=" ")
    embed.set_author(name=f"{ctx.author.name} {move_data['phrase']}")
    #embed.set_thumbnail(url=move_data['img']) this is the default maddie logo
    embed.set_thumbnail(url=ctx.author.avatar_url) #use their logo instead!
    lang = 'en'
    desc = get_translation(lang, 'description')
    embed.add_field(name=desc, value=f"{move_data['blob']}")
    addendum = None
    if move_data['requiresRolling']:
        addendum = handle_roll_ctx(character, embed, modifier, lang, ctx, move_data)
        #       embed.set_footer(text=" ")
        #       embed.set_author(name=f"{user} {phrase}")
        dicedisplay = True

        if dicedisplay:
            return embed, addendum
    return embed, ''

def get_modifier_from_character(labels, conditions, label, condition, user, lang):
    mod = 0
    character_label = ''
    character_condition = ''
    if condition and conditions[condition]:
        mod = -2
        character_condition = get_translation(lang, 'dice_rolling.condition_text')(condition, user)

    if label == CONDITIONS:
        conditions_count = 0
        for condition in conditions:
            if conditions[condition]:
                conditions_count += 1
                #Special case for newborn damaged condition which has been confirmed to give an extra +1
                if condition == 'damaged':
                    conditions_count += 1
        character_condition = get_translation(lang, 'dice_rolling.conditions_marked')(conditions_count, user)
        # Special case for newborn damaged condition which has been confirmed to give an extra +1
        if conditions['damaged']:
            character_condition = get_translation(lang, 'dice_rolling.conditions_marked')(conditions_count-1, user) + get_translation(lang, 'dice_rolling.damaged_marked')

        return (mod + conditions_count, character_condition, character_label)

    if label not in ['adult', 'basic', 'flat']:
        mod += labels[label][VALUE]
        character_label = get_translation(lang, 'dice_rolling.label')(label.title(), labels[label][VALUE])
    return (mod, character_condition, character_label)


def handle_roll(character, message, embed, num, mod, lang, label, condition, user):
    #character = get_character(message) #get it higher up instead
    character_label = ''
    character_condition = ''
    char_mod = 0
    command_mod = ''

    if character:
        user = character['characterName']
        (char_mod, character_condition, character_label) = get_modifier_from_character(character[LABELS], character[CONDITIONS], label, condition, user, lang)
#        logger.info("Accessing " + character['characterName'])
    num_calc = get_modified_num(mod, num)
    command_mod = num_calc #before the character mod is applied but after it's capped
    num_calc = get_cap(num_calc + char_mod)
    return add_result(embed, num_calc, mod, lang, character_label, character_condition, user, command_mod)

def handle_roll_ctx(character, embed, modifier, lang, ctx, move_data):
    #character = get_character(message) #get it higher up instead
    character_label = ''
    character_condition = ''
    char_mod = 0
    command_mod = ''

    if character:
        user = character['characterName']
        (char_mod, character_condition, character_label) = get_modifier_from_character(character[LABELS], character[CONDITIONS], move_data.get('label'), move_data.get('condition'), user, lang)
#        logger.info("Accessing " + character['characterName'])
    num_calc = get_modified_num_ctx(modifier)
    command_mod = num_calc #before the character mod is applied but after it's capped
    num_calc = get_cap_ctx(num_calc + char_mod)
    return add_result(embed, num_calc, modifier, lang, character_label, character_condition, command_mod)


def add_result (embed, num_calc, mod, lang, character_label, character_condition, user, command_mod=''):
    """
    Rolls dice, mutates embed with result, returns emoji
    corresponding to the dice components of the result.
    """
    #do dice rolling
    result1 = random.randrange(1,7) ##first d6
    result2 = random.randrange(1,7) ##second d6
    die1 = get_die(result1)
    die2 = get_die(result2)
    mod_emoji = get_mod_emoji(num_calc)
    result_tot = result1 + result2 + num_calc

    if mod == '-':
        modifier_to_show = ''
    elif type(mod) == int: # dumb case as when the slash verion runs this is a number, but for normal it's a +/- modifier
        if mod > -1:
            modifier_to_show = '+'
        elif mod <= -1:
            modifier_to_show = ''
    else:
        modifier_to_show = f' {mod}'

    calculation_title = get_translation(lang, 'dice_rolling.calculation_title')

    calculation = get_translation(lang, 'dice_rolling.calculation')(result1, result2, modifier_to_show, num_calc)
    if character_condition: calculation = character_condition + calculation
    if character_label: calculation = character_label + calculation
    result = get_translation(lang, 'dice_rolling.result')
    if command_mod: calculation = get_translation(lang, 'dice_rolling.command_modifier')(command_mod) + calculation
    embed.add_field(name=calculation_title, value=calculation, inline=False)
    embed.add_field(name=result, value=f"**{result_tot}**")

    return die1 + " " + die2 + " " + mod_emoji

def get_die (result):
    """
    Just does some sweet emoji lookups in the dictionary
    :param result: is the side of a 6 sided die you're looking for
    :return: is the id of the relevant emoji
    """
    for d in dice:
        if d[0] == result:
            emoji = f'<:{d[1]}:{d[2]}>'
    return emoji

def get_mod_emoji(mod_num):
    """
    :param mod_num: result form earlier command, lookup after being limited by cap and floor
    :return: modifier emoji
    """
    mod_emoji = ''
    for e in modifier_emojis:
        if e[0] == mod_num:
            mod_emoji = f'<:{e[1]}:{e[2]}>'
    return mod_emoji

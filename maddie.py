
# bot.py
import os
import discord
import random
import json
import re
import logging

from dotenv import load_dotenv

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO) #set logging level to INFO, DEBUG if we want the full dump
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a') #open log file in append mode
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
if __file__ == 'maddie2.py':TOKEN = os.getenv('DISCORD_TOKEN_DEV')
else:TOKEN = os.getenv('DISCORD_TOKEN')
logger.info (TOKEN)
client = discord.Client()

##Load in the existing moves
input_file = open ('data.json')
json_array = json.load(input_file)

##Setup the big sub
def mad_parse(msg,user):
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
    searchStr3 = r'[123456]'
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
    logger.info (msg + log_line)
 # figure out which type of modifier it is
    num_calc = int(0)
    if mod == '+': num_calc  = num 
    elif mod == '-' : num_calc = -1 * num
    else : num_calc = num
 # lookup a table for the big blob of text and a wee blob
    for p in json_array['moves']:
        if p['shortName'] == word:
            blob = p['blob']
            capital = p['capital']
            phrase = p['phrase']
            img = p['img']
            match = 1
    #Quiet mode
    searchStr4 = r'!!'
    result4 = re.search(searchStr4, msg)
    if result4: quiet = 1
#do dice rolling
    result1 = random.randrange(1,7) ##first d6
    result2 = random.randrange(1,7) ##second d6
    result_tot = result1 + result2 + num_calc #2 d6 + mod
#Ugly format blob!
    if match == 1 : #lets us ignore ! prefix commands that aren't in our list
        embed=discord.Embed(title=f"{capital}")
        embed.set_author(name=f"{user} {phrase}")
        embed.set_thumbnail(url=img)
        if quiet == 0: embed.add_field(name="Description", value=f"{blob}") # don't include the blob if we're in quiet mode (!!)
        embed.add_field(name="Calculation", value=f"Dice **{result1}** + **{result2}**, Label {mod} **{num}**", inline=False)
        embed.add_field(name="Result", value=f"**{result_tot}**")
        embed.set_footer(text=" ")

        return embed

    else:
        logger.info('no match found for '+msg)
        return 0


@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord!')
    servers = list(client.guilds)
    logger.info("Connected on "+str(len(client.guilds))+" servers:")
    for x in range(len(servers)):
        logger.info('   ' + servers[x-1].name)

#Listen for messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #answer a call for help
    elif message.content.startswith("!help"):
        log_line = message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
        logger.info(log_line)
        help_file = open("help","r")
        response = help_file.read() 
        await message.channel.send(response)
    #list moves
    elif message.content.startswith("!moves+"):
        response = '**Name - description, keyword, label**\n'
        for p in json_array['moves']:
            response = response + p['capital'].capitalize() + " - " + p['description'] + ", " + p['shortName'] + ", " + p['label'] + "\n "
        await message.channel.send(response) 
    elif message.content.startswith("!moves"):
        response = ''
        for p in json_array['moves']:
            response = response + p['shortName'] + ", "
        await message.channel.send(response) 
#remember generic ! should always be last in the tree
    elif message.content.startswith("!"):
        log_line = message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
        logger.info(log_line)
        response =  mad_parse(message.content, message.author.display_name)
        if response: 
            logger.info(response)
            await message.channel.send(embed=response)
client.run(TOKEN)

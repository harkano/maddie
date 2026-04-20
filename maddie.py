# bot.py
import os
import discord
import json
import logging

from dotenv import load_dotenv
from moves import get_moves
from parse import mad_parse
from command_handler import plain_command_handler, embed_command_handler
from config_interactions import get_dicedisplay
from discord.ext import commands

# --- Configure Logging ---
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
logger.info(TOKEN)

# Enable intents for discord.py 2.0+
intents = discord.Intents.default()
intents.message_content = True # Required to read message content for legacy ! commands

# We use commands.Bot now, which inherits from discord.Client,
# so we can use bot.tree.command (Slash commands) seamlessly alongside ! commands.
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    servers = list(bot.guilds)
    logger.info("Connected on "+str(len(bot.guilds))+" servers:")
    for x in range(len(servers)):
        logger.info('   ' + servers[x-1].name)
    
    # Sync slash commands with Discord globally
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        logger.error(f"Failed to sync slash commands: {e}")

def msg_log_line(message):
    if message.guild is not None:
        return message.guild.name + "|" + message.channel.name + "|" + message.author.name + "|" + message.content
    else:
        return "[Direct Message]" + "|" + message.author.name + "|" + message.content

#Listen for messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Since we are using commands.Bot, we MUST process commands
    # so that the discord.py library can handle events if we ever use `@bot.command`
    await bot.process_commands(message)

    # handle help and all of the playbook interactions
    if message.content.startswith("!"):
        response = plain_command_handler(message)

        if response:
            log_line = msg_log_line(message)
            logger.info(log_line)
            # The plain_command_handler might return a string or sometimes dict depending on execution
            if isinstance(response, str):
                await message.channel.send(response)
            else:
                await message.channel.send(content=str(response))
            return

        response = embed_command_handler(message)

        if response:
            log_line = msg_log_line(message)
            logger.info(log_line)
            if isinstance(response, discord.Embed):
                await message.channel.send(embed=response)
            else:
                await message.channel.send(content=str(response))
            return

    #answer a call for help
    if message.content.startswith("!help"):
        log_line = msg_log_line(message)
        logger.info(log_line)
        help_file = open("help", "r")
        response = help_file.read()

        await message.author.send(response)
        await message.channel.send("I have sent help to your PMs.")

    #list moves#
    if message.content.startswith("!"):
        move_list = get_moves(message)
        if move_list:
            if isinstance(move_list, str):
                await message.channel.send(move_list)
        #remember generic ! should always be last in the tree#
        else:
            log_line = msg_log_line(message)
            logger.info(log_line)
            response = mad_parse(message)
            if response:
                logger.info(response)
                (embed_response, addendum) = response
                
                if addendum is not None:
                    await message.channel.send(content=addendum, embed=embed_response)
                else:
                    await message.channel.send(embed=embed_response)
            else : logger.info('no match found for '+message.content)

# We include the slash commands here so they get registered on the bot.tree
import maddie_slash

bot.run(TOKEN)

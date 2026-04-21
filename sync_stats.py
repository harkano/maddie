import os
import json
import asyncio
import discord
from dotenv import load_dotenv
import logging
import sys

# Configure logging to output to standard out so it's easily visible when running
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('sync_stats')

load_dotenv()
# Note: Ensure you are using the correct environment variable for your bot token!
TOKEN = os.getenv('DISCORD_TOKEN') or os.getenv('STATS_TOKEN')
TOP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "adventures")
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "adventurers.json")

async def sync_data():
    logger.info("Initializing Discord Client...")
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    characters_data = []
    total_channels_with_data = 0
    
    channel_ids = set()
    user_ids = set()
    raw_characters = []

    logger.info(f"Scanning local adventures directory at: {TOP_DIR}")
    if os.path.exists(TOP_DIR):
        for channel_id_str in os.listdir(TOP_DIR):
            channel_path = os.path.join(TOP_DIR, channel_id_str)
            if os.path.isdir(channel_path):
                total_channels_with_data += 1
                try:
                    channel_id = int(channel_id_str)
                    channel_ids.add(channel_id)
                except ValueError:
                    pass
                
                for filename in os.listdir(channel_path):
                    if filename.endswith(".json") and filename != "settings.json":
                        file_path = os.path.join(channel_path, filename)
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                char_info = json.load(f)
                                
                                user_id_str = filename.replace(".json", "")
                                try:
                                    user_id = int(user_id_str)
                                    user_ids.add(user_id)
                                except ValueError:
                                    pass
                                
                                raw_characters.append({
                                    "channel_id": channel_id_str,
                                    "user_id": user_id_str,
                                    "char_info": char_info
                                })
                        except Exception as e:
                            logger.warning(f"Failed to read {file_path}: {e}")
                            continue
                            
        logger.info(f"Found {len(channel_ids)} distinct channels and {len(user_ids)} distinct users across {len(raw_characters)} characters.")
    else:
        logger.warning(f"Adventures directory not found at {TOP_DIR}. Nothing to sync.")
        return

    @client.event
    async def on_ready():
        logger.info(f"Logged in to Discord as {client.user}.")
        
        channel_names = {}
        guild_names = {}
        user_names = {}
        
        logger.info(f"Fetching names for {len(channel_ids)} channels from Discord API...")
        for i, cid in enumerate(channel_ids, 1):
            if i % 10 == 0:
                logger.info(f"  Processed {i}/{len(channel_ids)} channels...")
                
            channel = client.get_channel(cid)
            if not channel:
                try:
                    channel = await client.fetch_channel(cid)
                except discord.errors.Forbidden:
                    logger.debug(f"Missing access to channel {cid}")
                except discord.errors.NotFound:
                    logger.debug(f"Channel {cid} not found")
                except Exception as e:
                    logger.debug(f"Error fetching channel {cid}: {e}")
            
            if channel:
                channel_names[str(cid)] = channel.name
                if hasattr(channel, 'guild'):
                    guild_names[str(cid)] = channel.guild.name
                else:
                    guild_names[str(cid)] = "Direct Message"
            else:
                channel_names[str(cid)] = f"Unknown ({cid})"
                guild_names[str(cid)] = "Unknown Server"
                
        logger.info(f"Fetching names for {len(user_ids)} users from Discord API...")
        for i, uid in enumerate(user_ids, 1):
            if i % 10 == 0:
                logger.info(f"  Processed {i}/{len(user_ids)} users...")
                
            user = client.get_user(uid)
            if not user:
                try:
                    user = await client.fetch_user(uid)
                except Exception as e:
                    logger.debug(f"Error fetching user {uid}: {e}")
            
            if user:
                user_names[str(uid)] = user.name
            else:
                user_names[str(uid)] = f"Unknown ({uid})"
                
        logger.info("Assembling final dataset...")
        for raw in raw_characters:
            cid = raw["channel_id"]
            uid = raw["user_id"]
            cinfo = raw["char_info"]
            
            player_name = cinfo.get("playerName")
            if not player_name or player_name == "Unknown":
                player_name = user_names.get(uid, f"Unknown ({uid})")
            
            characters_data.append({
                "guild_name": guild_names.get(cid, "Unknown Server"),
                "channel_name": channel_names.get(cid, f"Unknown ({cid})"),
                "player_name": player_name,
                "character_name": cinfo.get("characterName", "Unknown"),
                "playbook": str(cinfo.get("playbook", "Unknown")).capitalize(),
                "potential": cinfo.get("potential", 0)
            })
            
        output_data = {
            "active_channels": total_channels_with_data,
            "total_characters": len(characters_data),
            "characters": characters_data
        }
        
        logger.info(f"Writing {len(characters_data)} rows to {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4)
            
        logger.info("Sync complete. Closing Discord client...")
        await client.close()

    logger.info("Starting Discord client connection...")
    if not TOKEN:
        logger.error("No Discord token found. Check your .env file.")
        return
        
    await client.start(TOKEN)
    logger.info("Script finished successfully.")

if __name__ == "__main__":
    asyncio.run(sync_data())

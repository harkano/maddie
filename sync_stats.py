import os
import json
import asyncio
import discord
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sync_stats')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TOP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "adventures")
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "adventurers.json")

async def sync_data():
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    characters_data = []
    total_channels_with_data = 0
    
    channel_ids = set()
    user_ids = set()
    raw_characters = []

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
                        except Exception:
                            continue

    @client.event
    async def on_ready():
        logger.info(f"Logged in as {client.user}. Fetching data...")
        
        channel_names = {}
        guild_names = {}
        user_names = {}
        
        for cid in channel_ids:
            channel = client.get_channel(cid)
            if not channel:
                try:
                    channel = await client.fetch_channel(cid)
                except Exception:
                    pass
            
            if channel:
                channel_names[str(cid)] = channel.name
                if hasattr(channel, 'guild'):
                    guild_names[str(cid)] = channel.guild.name
                else:
                    guild_names[str(cid)] = "Direct Message"
            else:
                channel_names[str(cid)] = f"Unknown ({cid})"
                guild_names[str(cid)] = "Unknown Server"
                
        for uid in user_ids:
            user = client.get_user(uid)
            if not user:
                try:
                    user = await client.fetch_user(uid)
                except Exception:
                    pass
            
            if user:
                user_names[str(uid)] = user.name
            else:
                user_names[str(uid)] = f"Unknown ({uid})"
                
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
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4)
            
        logger.info(f"Successfully wrote {len(characters_data)} characters to {OUTPUT_FILE}")
        await client.close()

    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(sync_data())
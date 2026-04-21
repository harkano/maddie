import os
import json
import asyncio
from flask import Flask, render_template_string
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

app = Flask(__name__)

# The top level directory to store all files
TOP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "adventures")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maddie Stats Dashboard</title>
    <!-- AG Grid -->
    <script src="https://cdn.jsdelivr.net/npm/ag-grid-community/dist/ag-grid-community.min.js"></script>
    <style>
        body { font-family: sans-serif; margin: 40px; background-color: #f4f4f9; color: #333; }
        h1 { color: #53B0B9; }
        .dashboard-container { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 30px; }
        .card {
            background-color: white; padding: 20px; border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 250px; text-align: center;
        }
        .card h2 { margin-top: 0; font-size: 1.2em; color: #666; }
        .card .value { font-size: 2.5em; font-weight: bold; color: #53B0B9; }
        
        #myGrid {
            height: 600px;
            width: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .loading { text-align: center; color: #888; font-style: italic; }
    </style>
</head>
<body>

    <h1>Maddie Stats Dashboard</h1>
    
    <div class="dashboard-container">
        <div class="card">
            <h2>Active Channels</h2>
            <div class="value">{{ active_channels }}</div>
        </div>
        <div class="card">
            <h2>Total Characters</h2>
            <div class="value">{{ total_characters }}</div>
        </div>
    </div>
    
    <h2>Character Database</h2>
    <div id="myGrid" class="ag-theme-alpine"></div>
    
    <script>
        const rowData = {{ characters_json | safe }};
        
        const gridOptions = {
            columnDefs: [
                { field: "guild_name", headerName: "Server", filter: true, sortable: true },
                { field: "channel_name", headerName: "Channel", filter: true, sortable: true },
                { field: "player_name", headerName: "Player Name", filter: true, sortable: true },
                { field: "character_name", headerName: "Character Name", filter: true, sortable: true },
                { field: "playbook", headerName: "Playbook", filter: true, sortable: true },
                { field: "potential", headerName: "Potential", filter: true, sortable: true, width: 120 }
            ],
            defaultColDef: {
                flex: 1,
                minWidth: 100,
                resizable: true,
            },
            rowData: rowData,
            pagination: true,
            paginationPageSize: 20
        };

        document.addEventListener('DOMContentLoaded', () => {
            const gridDiv = document.querySelector('#myGrid');
            new agGrid.Grid(gridDiv, gridOptions);
        });
    </script>

</body>
</html>
"""

async def fetch_discord_data():
    """
    Spins up a temporary discord client to fetch names for all IDs found in the filesystem.
    """
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    characters_data = []
    total_channels_with_data = 0
    
    # We need to collect the IDs first so we can batch query them from the API
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
                
                # Scan for json files inside this channel directory
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
                            # Skip bad files
                            continue

    # We will hook into the on_ready event to do our fetching once logged in, 
    # and then gracefully shut down the bot.
    @client.event
    async def on_ready():
        nonlocal characters_data
        
        channel_names = {}
        guild_names = {}
        user_names = {}
        
        # Attempt to fetch channels and guilds
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
                
        # Attempt to fetch users
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
                
        # Assemble final dataset
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
            
        await client.close()

    # Run the client to grab the data, then close it immediately
    await client.start(TOKEN)
    
    return total_channels_with_data, characters_data

@app.route('/')
def index():
    # Execute the Discord bot login lifecycle to retrieve the names synchronously for the HTTP response
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    total_channels, characters_data = loop.run_until_complete(fetch_discord_data())
    loop.close()

    return render_template_string(
        HTML_TEMPLATE, 
        active_channels=total_channels, 
        total_characters=len(characters_data),
        characters_json=json.dumps(characters_data)
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

import os
import json
from flask import Flask, render_template_string

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
                { field: "channel_id", headerName: "Channel ID", filter: true, sortable: true },
                { field: "player_id", headerName: "Player ID", filter: true, sortable: true },
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

@app.route('/')
def index():
    total_channels_with_data = 0
    characters_data = []

    if os.path.exists(TOP_DIR):
        for channel_id in os.listdir(TOP_DIR):
            channel_path = os.path.join(TOP_DIR, channel_id)
            if os.path.isdir(channel_path):
                total_channels_with_data += 1
                
                # Scan for json files inside this channel directory
                for filename in os.listdir(channel_path):
                    if filename.endswith(".json") and filename != "settings.json":
                        file_path = os.path.join(channel_path, filename)
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                char_info = json.load(f)
                                
                                player_id = filename.replace(".json", "")
                                
                                # We can extract all relevant data here
                                characters_data.append({
                                    "channel_id": channel_id,
                                    "player_id": player_id,
                                    "player_name": char_info.get("playerName", "Unknown"),
                                    "character_name": char_info.get("characterName", "Unknown"),
                                    "playbook": str(char_info.get("playbook", "Unknown")).capitalize(),
                                    "potential": char_info.get("potential", 0)
                                })
                        except Exception as e:
                            # Skip bad files
                            continue

    return render_template_string(
        HTML_TEMPLATE, 
        active_channels=total_channels_with_data, 
        total_characters=len(characters_data),
        characters_json=json.dumps(characters_data)
    )

if __name__ == '__main__':
    # Use port 5000 by default, allowing external access if needed
    app.run(host='0.0.0.0', port=5000, debug=True)

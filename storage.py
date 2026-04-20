import json
import os
import logging
from pathlib import Path

logger = logging.getLogger('discord')

# The top level directory to store all files
TOP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "adventures")

def get_s3_client():
    # Return anything as a dummy client to avoid breaking usages that expect an object
    return True

def info_from_s3(key, s3_client=None):
    if not key:
        return None
    
    file_path = os.path.join(TOP_DIR, f"{key}.json")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = json.load(file)
            
            # Handle Replicate functionality
            if content.get('replicate_key'):
                repl_key = content['replicate_key']
                split_key = key.split("/")
                
                # In the old code: key = split_key[0] + "/" + file['Metadata']['replicate'] + "/" + split_key[2]
                new_key = f"{split_key[0]}/{repl_key}/{split_key[2]}"
                new_file_path = os.path.join(TOP_DIR, f"{new_key}.json")
                try:
                    with open(new_file_path, "r", encoding="utf-8") as repl_file:
                        repl_content = json.load(repl_file)
                        repl_content['replicate_key'] = new_key
                        return repl_content
                except FileNotFoundError:
                    return None
            return content
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.error(f'An error occurred while reading local file:\n{e}')
        raise e

def get_files_from_dir(key, s3_client=None):
    if not key:
        return {"Contents": []}
    
    dir_path = os.path.join(TOP_DIR, key)
    contents = []
    if os.path.exists(dir_path):
        for root, _, files in os.walk(dir_path):
            for file_name in files:
                if file_name.endswith('.json'):
                    # The S3 code expects something like a Key back
                    rel_path = os.path.relpath(os.path.join(root, file_name), TOP_DIR).replace("\\", "/")
                    # Remove the .json extension to match old behavior
                    contents.append({"Key": rel_path[:-5]})
    return {"Contents": contents}

def get_char_files_from_dir(key, s3_client=None):
    if not key:
        return
    
    dir_path = os.path.join(TOP_DIR, key)
    if os.path.exists(dir_path):
        for root, _, files in os.walk(dir_path):
            for file_name in files:
                if file_name.endswith('.json'):
                    rel_path = os.path.relpath(os.path.join(root, file_name), TOP_DIR).replace("\\", "/")
                    # S3 returned the key with .json but we used to strip it?
                    # The old code returned content.get('Key') which had .json
                    yield rel_path[:-5]

def upload_to_s3(content, key, s3_client=None):
    # Take the replicate key from the json, kill it and move it to metadata in old version
    # Here we just leave it in the JSON content
    
    actual_key = key
    if content.get('replicate_key'):
        actual_key = content['replicate_key']
        # We don't pop it so it saves in the file, simulating metadata
        
    file_path = os.path.join(TOP_DIR, f"{actual_key}.json")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(content, file, indent=4)
        
    logger.info(f'Finished writing to {actual_key}')

def s3_delete(key, s3_client=None):
    file_path = os.path.join(TOP_DIR, f"{key}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f'Deleted file {key}')

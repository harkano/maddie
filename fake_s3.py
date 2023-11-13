# Maddie currently assumes the existence of an S3 bucket we have access to,
# which is inconvenient for testing.
# Since it's too annoying to go through changing references to s3 specific methods right now,
# we're just gonna fake it out.
import json
import os

# A fake client class.
# All the methods in this module take this, instead of an s3 client from boto3.
# Instead of using S3, we just use a directory.
class FakeS3Client:
    def __init__(self):
        # This needs to end with `/`.
        self._top_dir = "/tmp/maddie/"

def get_s3_client():
    return FakeS3Client()

# Note that the `key` argument is `f"adventures/{channel_id}/{author_id}"`.
# It's really a relative file path.
def info_from_s3(key, s3_client):
    try:
        file = open(s3_client._top_dir + f"{key}.json")
        with file:
            return json.load(file)
    except FileNotFoundError:
        return None

# TODO: implement this, so the `/me Show Party` command works
# when USE_FAKE_S3="true".
def get_char_files_from_dir(key, s3_client):
    pass


def next(it):
    for x in it:
        return x

# Yep, just listing files.
def get_files_from_dir(key, s3_client):
    # Since the usage of this thing doesn't perform any indexing,
    # we should be able to get away with not actually making this into a list.
    par, _, names = next(os.walk(s3_client._top_dir + key))
    files = [ { "Key": f"{key}/{x}" } for x in names ]
    return { "Contents": files }

# I fail to see why this is a necessary abstraction,
# but the `s3_utils` module defines it.
def get_bytes_from_json(json_to_parse):
    return bytearray(json.dumps(json_to_parse), 'latin-1')

def upload_to_s3(content, key, s3_client):
    with open(s3_client._top_dir + key + '.json', 'w') as file:
        file.write(json.dumps(content))

def s3_delete(key, s3_client):
    os.remove(s3_client._top_dir + key + '.json')

# Conditionally use either S3 or local temporary filesystem.
from dotenv import load_dotenv
import os
load_dotenv()
# TODO: consider exactly how configuration should be shaped for this bot
if not os.getenv('USE_FAKE_S3') == 'true':
    from s3_utils import *
else:
    from fake_s3 import *

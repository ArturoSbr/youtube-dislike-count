# Libraries
import os
from dotenv import load_dotenv
from youtube import channel

# Load API_KEY
load_dotenv()
key = os.getenv('API_KEY')

# Search videos
yt = channel()

test = yt.channel_statistics(channelId='UChqUTb7kYRX8-EiaN3XFrSQ', key=key)
print(test)
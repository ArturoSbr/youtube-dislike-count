# Libraries
import os
from dotenv import load_dotenv
from youtube import channel

# Load API_KEY
load_dotenv()
key = os.getenv('API_KEY')

# Search videos
cnn = channel(id='UCupvZG-5ko_eiXAupbDfxWw', key=key)

vids = cnn.get_videos(category=25, date0='2021-11-01T00:00:00', date1='2021-11-09T23:59:59')
print(len(vids))
print(vids)
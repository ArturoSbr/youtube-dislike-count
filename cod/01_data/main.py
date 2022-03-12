# Libraries
import os
from dotenv import load_dotenv
from youtube import channel, video

# Load API_KEY
load_dotenv()
key = os.getenv('API_KEY')

# Declare objects
cnn = channel(id='UCupvZG-5ko_eiXAupbDfxWw', key=key)
vid = video(id='ewKg8DkwcLc', key=key)

# WORKS: channel.get_info()
# print(cnn.get_info())
# print(cnn.name

# WORKS: channel.get_videos()
# vids = cnn.get_videos(category=25, date0='2021-11-01T00:00:00', date1='2021-11-09T23:59:59')
# print(len(vids))
# print(vids)

# WORKS: video.get_details()
# print(vid.get_details())

# TEST: video.get_comments()
# comments = vid.get_comments()
# print(len(comments))
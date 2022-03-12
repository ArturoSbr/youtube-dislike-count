# Libraries
import os
from dotenv import load_dotenv
from youtube import channel, video

# Load API_KEY
load_dotenv()
key = os.getenv('API_KEY')

# Declare objects
cnn = channel(id='UCupvZG-5ko_eiXAupbDfxWw', key=key)   # CNN's channel
vid = video(id='ewKg8DkwcLc', key=key)                  # CNN's video on Rudy Giuliani

# Get CNN's general information
print(cnn.get_info())
print(cnn.name)

# Get the IDs of videos uploaded by CNN between two dates
vids = cnn.get_videos(category=25, date0='2021-10-31T00:00:00', date1='2021-10-31T23:59:59')
print(len(vids))

# Get some of the video's attributes
print(vid.get_details())

# Fetch all the comments posted on the video
comments = vid.get_comments()
print(len(comments))
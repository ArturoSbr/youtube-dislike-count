# TODO Dump comments per page
"""
{
  "items": [
    {
      "snippet": {
        "topLevelComment": {
          "snippet": {
            "textOriginal": "Watch Bundesliga Highlights on YouTube!\n► Sub now 👉 https://redirect.bundesliga.com/_bwCS",
            "publishedAt": "2022-03-12T22:23:29Z"
          }
        }
      }
    },
    {
      "snippet": {
        "topLevelComment": {
          "snippet": {
            "textOriginal": "Schade FC BAYERN ... hatten nicht viel Glueck",
            "publishedAt": "2022-03-14T13:14:10Z"
          }
        }
      }
    },
  ]
}
"""

"""
{
    "videoId":"videoidvideoidvideoid",
    "pageToken":"tokentokentokentoken",
    "comments":{
        "comment1":{
            "date":"2021-11-09",
            "text":"I hate this channel so much"
        },
        "comment2":{
            "date":"2021-11-09",
            "text":"I miss Belgium"
        }
 }
"""

# Libraries
import json
import requests

# Channel class
class channel():
    # Initialize channel
    def __init__(self, id=None, key=None):
        self.id = id
        self.key = key
        self.name = None

    # Get channel's title, join date and metrics
    def get_info(self):
        url = 'https://youtube.googleapis.com/youtube/v3/channels?' + \
            'part=snippet&' + \
            'part=statistics&' + \
            f'id={self.id}&' + \
            'fields=' + \
                'items(' + \
                    'snippet%2Ftitle%2C' + \
                    'snippet%2FpublishedAt%2C' + \
                    'statistics%2FviewCount)' + \
            f'&key={self.key}'
        r = json.loads(requests.get(url).text)['items'][0]
        self.name = r['snippet']['title']
        return [r['snippet']['title'], r['snippet']['publishedAt'][:10], r['statistics']['viewCount']]
    
    # Get channel's videos between two dates
    def get_videos(self, category=25, date0=None, date1=None):
        date0 = date0.replace(':','%3A')
        date1 = date1.replace(':','%3A')
        ret = []

        # First page
        url0 = 'https://youtube.googleapis.com/youtube/v3/search?' + \
            'part=id&' + \
            f'channelId={self.id}&' + \
            'maxResults=50&' + \
            'order=relevance&' + \
            f'publishedAfter={date0}Z&' + \
            f'publishedBefore={date1}Z&' + \
            'safeSearch=none&' + \
            'type=video&' + \
            f'videoCategoryId={25}&' + \
            'fields=' + \
                'nextPageToken%2C%20' + \
                'items(id%2FvideoId)&' + \
            f'key={self.key}'
        r = json.loads(requests.get(url0).text)['items']
        try:
            npt = r['nextPageToken']
        except:
            npt = None
        for item in r:
            ret.append(item['id']['videoId'])

        # Subsequent pages
        while npt is not None:
            # Get next URL using previous token
            url = url0 + f'&pageToken={npt}'
            r = json.loads(requests.get(url).text)['items']
            # Update next page's token
            try:
                npt = r['nextPageToken']
            except:
                npt = None
            # Extract all comments on page
            for item in r:
                ret.append(item['id']['videoId'])
        
        # Return all videos
        return ret

# Video class
class video():
    # Initialize object
    def __init__(self, id=None, key=None):
        self.id = id
        self.key = key

    # Get video's details (title, tags, etc)
    def get_details(self):
        url = 'https://youtube.googleapis.com/youtube/v3/videos?' + \
            'part=snippet&' + \
            'part=contentDetails&' + \
            f'id={self.id}&' + \
            'fields=' + \
                'items(' + \
                    'snippet%2FpublishedAt%2C%20' + \
                    'snippet%2Ftitle%2C%20' + \
                    'snippet%2Fdescription%2C%20' + \
                    'snippet%2Ftags%2C%20' + \
                    'snippet%2FliveBroadcastContent%2C%20' \
                    'contentDetails%2Fduration%2C%20' + \
                    'contentDetails%2Fdefinition%2C%20)&' + \
            f'key={self.key}'
        r = json.loads(requests.get(url).text)['items'][0]
        ret = {**r['snippet'], **r['contentDetails']}
        try:
            ret['tags'] = ', '.join(ret['tags'])
        except:
            ret['tags'] = ''
        return dict(sorted(ret.items()))
    
    # Get video's top-level comments
    def get_comments(self):
        
        # Initialize list
        ret = []

        # First page
        url0 = 'https://youtube.googleapis.com/youtube/v3/commentThreads?' + \
            'part=snippet&' + \
            'maxResults=50&' + \
            'moderationStatus=published&' + \
            'order=time&' + \
            'textFormat=plainText&' + \
            f'videoId={self.id}&' + \
            'fields=' + \
                'nextPageToken%2C%20' + \
                'items(' + \
                    'snippet%2FtopLevelComment%2Fsnippet%2FtextOriginal%2C%20' + \
                    'snippet%2FtopLevelComment%2Fsnippet%2FpublishedAt)&' + \
            f'key={self.key}'
        r = json.loads(requests.get(url=url0).text)

        # Get comments (if enabled)
        try:
            # Declare next page's token
            try:
                npt = r['nextPageToken']
            except:
                npt = None
            # Extract all comments from current page
            for item in r['items']:
                ret.append(item['snippet']['topLevelComment']['snippet'])
            
            # Subsequent pages
            while npt is not None:
                # Get next URL using previous token
                url = url0 + f'&pageToken={npt}'
                r = json.loads(requests.get(url=url).text)
                # Update next page's token
                try:
                    npt = r['nextPageToken']
                except:
                    npt = None
                # Extract all comments
                for item in r['items']:
                    ret.append(item['snippet']['topLevelComment']['snippet'])
        
        # Case when comments are disabled
        except:
            print(r['error']['errors'][0]['reason'], f'on videoId = {self.id}')
        
        # Return all comments
        return ret
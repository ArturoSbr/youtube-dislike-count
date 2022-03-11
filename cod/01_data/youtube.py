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

        # Get first page
        url = 'https://youtube.googleapis.com/youtube/v3/search?' + \
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
        r = json.loads(requests.get(url).text)
        try:
            npt = r['nextPageToken']
        except:
            npt = None
        for i in range(len(r['items'])):
            ret.append(r['items'][i]['id']['videoId'])

        # Get subsequent requests
        while npt is not None:
            url = 'https://youtube.googleapis.com/youtube/v3/search?' + \
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
                f'pageToken={npt}&' + \
                f'key={self.key}'
            r = json.loads(requests.get(url).text)
            try:
                npt = r['nextPageToken']
            except:
                npt = None
            for i in range(len(r['items'])):
                ret.append(r['items'][i]['id']['videoId'])
        return ret

class video():
    # Initialize object
    def __init__(self, id=None, key=None):
        self.id = id

    # Get video's details (title, tags, etc)
    def get_details(self):
        """
        https://youtube.googleapis.com/youtube/v3/videos?
        part=snippet&
        part=contentDetails&
        id=uDjeOcBPxfk&
        fields=
            items(
                snippet%2FpublishedAt%2C%20
                snippet%2Fdescription%2C%20
                snippet%2Ftags%2C%20
                snippet%2FliveBroadcastContent%2C%20
                contentDetails%2Fduration%2C%20
                contentDetails%2Fdefinition&
        key=[YOUR_API_KEY]
        """
    
    # Get video's top-level comments
    def get_comments(self):
        """
        https://youtube.googleapis.com/youtube/v3/commentThreads?
        part=snippet&
        maxResults=50&
        moderationStatus=published&
        order=time&
        textFormat=plainText&
        videoId=uDjeOcBPxfk&
        fields=
            nextPageToken%2C%20
            items(
                snippet%2FtopLevelComment%2Fsnippet%2FtextOriginal%2C%20
                snippet%2FtopLevelComment%2Fsnippet%2FpublishedAt)&
        key=[YOUR_API_KEY]
        """
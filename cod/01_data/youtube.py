# Libraries
import json
import requests

# Youtube class
class channel():
    # Initialize channel
    def __init__(self, id=None, key=None):
        self.id = id
        self.key = key
        self.name = None
        self.joined = None

    # Get channel's title, join date and metrics
    def get_statistics(self):
        url = 'https://youtube.googleapis.com/youtube/v3/channels?' + \
            f'part=statistics&part=snippet&id={self.id}&' + \
            f'fields=items(statistics%2Csnippet%2Ftitle%2Csnippet%2FpublishedAt)&key={self.key}'
        r = json.loads(requests.get(url).text)
        self.name = r['items'][0]['snippet']['title']
        self.joinDate = r['items'][0]['snippet']['publishedAt'][:10]
        return r['items'][0]['statistics']
    
    # Get channel's videos between two dates
    def get_videos(self, date0=None, date1=None):
        date0 = date0.replace(':','%3A')
        date1 = date1.replace(':','%3A')
        ret = []

        # Get first request
        url = 'https://youtube.googleapis.com/youtube/v3/search?' + \
            f'part=id&part=snippet&channelId={self.id}&maxResults=50&order=relevance&' + \
            f'publishedAfter={date0}Z&publishedBefore={date1}Z&' + \
            'safeSearch=none&type=video&videoCategoryId=25&' + \
            f'fields=items(id%2FvideoId)%2Citems(snippet%2FpublishedAt)&key={self.key}'
        print(url)
        r = json.loads(requests.get(url).text)
        try:
            npt = r['nextPageToken']
        except:
            npt = None
        for i in range(len(r['items'])):
            ret.append((r['items'][i]['id']['videoId'], r['items'][i]['snippet']['publishedAt']))

        # Get subsequent requests
        while npt is not None:
            url = 'https://youtube.googleapis.com/youtube/v3/search?' + \
                f'part=id&part=snippet&channelId={self.id}&maxResults=50&order=relevance&' + \
                f'publishedAfter={date0}Z&publishedBefore={date1}Z&' + \
                f'safeSearch=none&type=video&videoCategoryId=25&pageToken={npt}' + \
                f'fields=items(id%2FvideoId)%2Citems(snippet%2FpublishedAt)&key={self.key}'
            print(url)
            r = json.loads(requests.get(url).text)
            try:
                npt = r['nextPageToken']
            except:
                npt = None
            for i in range(len(r['items'])):
                ret.append((r['items'][i]['id']['videoId'], r['items'][i]['snippet']['publishedAt']))
        
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
            items(snippet%2FpublishedAt)%2C%20
            items(snippet%2Ftitle)%2C%20
            items(snippet%2Fdescription)%2C%20
            items(snippet%2Ftags)%2C%20
            items(snippet%2FliveBroadcastContent)%2C%20
            items(contentDetails%2Fduration)%2C%20
            items(contentDetails%2Fdefinition)&
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
            items(snippet%2FtopLevelComment%2Fsnippet%2FtextOriginal)%2C%20
            items(snippet%2FtopLevelComment%2Fsnippet%2FpublishedAt)&
        key=[YOUR_API_KEY]
        """
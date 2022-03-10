# Libraries
import json
import requests

# Youtube class
class channel():
    # Initialize
    def __init__(self):
        self.name = None
        self.joined = None

    # Get channel's title, join date and metrics
    def statistics(self, channelId=None, key=None):
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=statistics&part=snippet&id={channelId}&' + \
            f'fields=items(statistics%2Csnippet%2Ftitle%2Csnippet%2FpublishedAt)&key={key}'
        r = json.loads(requests.get(url).text)
        self.name = r['items'][0]['snippet']['title']
        self.joinDate = r['items'][0]['snippet']['publishedAt'][:10]
        return r['items'][0]['statistics']
    
    # Get channel's videoIds between two dates
    def videos(self, key=None, channelId=None, date0=None, date1=None):
        # TODO get next page until end
        date0 = date0.replace(':','%3A')
        date1 = date1.replace(':','%3A')
        url = 'https://youtube.googleapis.com/youtube/v3/search?' + \
            f'part=id&channelId={channelId}&maxResults=50&order=relevance&' + \
            f'publishedAfter={date0}Z&publishedBefore={date1}Z&' + \
            f'safeSearch=none&type=video&videoCategoryId=25&' + \
            f'fields=items(id%2FvideoId)&key={key}'
        return json.loads(requests.get(url).text)

"""
https://youtube.googleapis.com/youtube/v3/search?part=id&
part=snippet&
channelId=UChqUTb7kYRX8-EiaN3XFrSQ&
maxResults=50&order=relevance
&publishedAfter=2021-11-09T00%3A00%3A00Z&
publishedBefore=2021-11-09T23%3A59%3A59Z&
safeSearch=none&
type=video&
fields=nextPageToken%2Citems(id%2FvideoId)%2Citems(snippet%2FpublishedAt)&
key=[YOUR_API_KEY]
"""
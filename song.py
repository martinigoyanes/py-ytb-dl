import youtube_dl
import time
from googleapiclient.discovery import build

YB_KEY = 'AIzaSyD6cQWDR1VZpeVylYtDY5Q3I0jopaIyokg'


class Song:
    artists = []

    def __init__(self, name, video_url, artists):
        self.name = name
        self.video_url = video_url
        self.artists = artists

    # * Downloads video from youtube and transforms it into mp3 file, deletes original video
    def download(self):
        params = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        downloader = youtube_dl.YoutubeDL(params)
        downloader.download(self.video_url)

    def search(self):
        youtube = build('youtube', 'v3', developerKey=YB_KEY)
        query = self.name
        for artist in self.artists:
            query = query + " " + artist
        query = query + " Official Audio"
        req = youtube.search().list(part='id', q=query,
                                    maxResults=1, type='video',
                                    fields='items/id/videoId')
        resp = req.execute()
        video_id = resp['items'][0]['id']['videoId']
        self.video_url = [f'https://www.youtube.com/watch?v={video_id}']

    def thread_handler(self):
        """ self.search()
        self.download() """
        time.sleep(3)
        print("thread running")

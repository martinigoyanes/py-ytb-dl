import youtube_dl
from googleapiclient.discovery import build

YB_API_KEY = 'AIzaSyB03vuHLAD9t05azz8qjv-bfdgtgZwhjY0'

class Song:

    def __init__(self, name, video_url, artist):
        self.name = name
        self.video_url = video_url
        self.artist = artist

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
        youtube = build('youtube', 'v3', developerKey=YB_API_KEY)
        req = youtube.search().list(part='id', q=self.name, maxResults=25, type='video')
        resp = req.execute()

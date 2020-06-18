import youtube_dl
import time
import config



class Song:
    artists = []

    def __init__(self, name, video_url, artists):
        self.name = name
        self.video_url = video_url
        self.artists = artists
        self.downloaded = False

    # * Downloads video from youtube and transforms it into mp3 file, deletes original video
    def download(self):
        params = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            ],
            'outtmpl' : '/Users/martin/Desktop/%(title)s.%(ext)s'
        }
        downloader = youtube_dl.YoutubeDL(params)
        downloader.download(self.video_url)

    def search(self,youtube):
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

    def thread_handler(self, youtube,song_list_len):
        self.search(youtube)
        self.download()
        
        config.downloaded_songs_lock.acquire()
        self.downloaded = True
        config.downloaded_songs += 1
        
        print( '\"' + self.name + '\" downloaded.')
        
        if config.downloaded_songs < song_list_len:
            print( "[" + str(config.downloaded_songs) + "/" + str(song_list_len) + "]" + " songs downloading....")
        else:
            print("Finished downloading " + str(song_list_len) + " songs")

        config.downloaded_songs_lock.release()
        

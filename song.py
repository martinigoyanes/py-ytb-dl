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
    def download(self,verbose=True):
        outformat = f'/Users/martin/Desktop/{self.name}'
        for artist in self.artists:
            outformat += f' - {artist}'
        outformat += '.%(ext)s'

        params = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            ],
            'outtmpl' : outformat,
            'retries': 10,
            'quiet': not verbose 
        }

        downloader = youtube_dl.YoutubeDL(params)
        downloader.download(self.video_url)

    def search(self):
        query = self.name
        for artist in self.artists:
            query = query + " " + artist
        query = query + " Official Audio"
        req = config.youtube.search().list(part='id', q=query,
                                    maxResults=1, type='video',
                                    fields='items/id/videoId')
        resp = req.execute()
        video_id = resp['items'][0]['id']['videoId']
        self.video_url = [f'https://www.youtube.com/watch?v={video_id}']
        # For debugging
        with config.url_file_lock and open('vide_urls.txt', 'a+') as url_file:
            url_file.write(f'{self.name} - {self.artists} - {self.video_url}\n')       

    def thread_handler(self, song_list_len):
        # self.search()
        #* If there is any error downloading write the problematic song name - artist - videourl to file
        try:
            self.download()
        except Exception:
            print(f'ERROR: Could NOT download {self.name} - {self.artists}\n') 
            with config.error_file_lock and open('failed_songs.txt', 'a+') as error_file:
                error_file.write(f'{self.name} - {self.artists} - {self.video_url}\n')       
        
        else:
            with config.downloaded_songs_lock:
                self.downloaded = True
                config.downloaded_songs += 1
                
                print( '\"' + self.name + '\" downloaded.')
                
                if config.downloaded_songs < song_list_len:
                    print( "[" + str(config.downloaded_songs) + "/" + str(song_list_len) + "]" + " songs downloading....")
                else:
                    print("Finished downloading " + str(song_list_len) + " songs")

        

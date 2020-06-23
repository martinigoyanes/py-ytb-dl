import youtube_dl
import time
import config
import glob
import os
from mutagen.id3 import ID3, APIC, USLT, _util
from mutagen.mp3 import EasyMP3
from mutagen import File
from urllib.request import urlopen



class Song:
    artists = []
    metadata = dict()
    def __init__(self, name, video_url, artists, cover, album):
        self.name = name
        self.video_url = video_url
        self.artists = artists
        self.downloaded = False
        self.fullname = name 
        for artist in artists:
            self.fullname += f' - {artist}'
        self.outtemplate = f'/Users/martin/Desktop/{self.fullname}.%(ext)s' 
        self.fullpath = f'/Users/martin/Desktop/{self.fullname}.mp3' 
        self.thread = None
        self.failed = False
        self.metadata = {
            'cover_url': cover,
            'album':album
        }

    # * Downloads video from youtube and transforms it into mp3 file, deletes original video
    def download(self,song_list_len,verbose=True):
        with config.started_songs_lock:
            config.started_songs += 1
            print( self.name +" has started. [" + str(config.started_songs) + "/" +
                  str(song_list_len) + "]" + " songs started downloading....")

        params = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            ],
            'outtmpl' : self.outtemplate,
            'retries': 10,
            # 'quiet': not verbose
        }

        if self.failed is True:
            print(f'Retrying {self.fullname} ....')
            
        downloader = youtube_dl.YoutubeDL(params)
        downloader.download(self.video_url)

    def search(self):
        query = self.fullname + " Official Audio"
        req = config.youtube.search().list(part='id', q=query,
                                    maxResults=1, type='video',
                                    fields='items/id/videoId')
        resp = req.execute()
        video_id = resp['items'][0]['id']['videoId']
        self.video_url = [f'https://www.youtube.com/watch?v={video_id}']
        
        # For debugging
        # album = self.metadata['album']
        # cover_url = self.metadata['cover_url']
        # with config.url_file_lock and open('video_urls.txt', 'a+') as url_file:
        #     url_file.write(f'{self.name} %% {self.artists} %% {album} %% {cover_url} %% {self.video_url}\n')       

    def thread_handler(self, song_list_len,verbose):
        # try:
        #     # self.search()
        #     pass
        # except Exception as e:
        #     print(f'ERROR while searching for {self.fullname}. Reason -> {str(e)}\n') 
        #     self.failed = True
        #     with config.started_songs_lock:
        #         config.started_songs -= 1
        #         return
        try:
            self.download(song_list_len, verbose=verbose)
        except Exception as e:
            print(f'ERROR: Could NOT download {self.fullname}. Reason -> {str(e)}\n') 
            # If there is any error downloading write the problematic song name %% artist %% videourl to file
            # with config.error_file_lock and open('failed_songs.txt', 'a+') as error_file:
            #     error_file.write(f'{self.name} %% {self.artists} %% {self.video_url}\n')       

            #* There has been an error so remove any data that has been downloaded so in next iter there's no confusion
            self.failed = True
            with config.started_songs_lock:
                config.started_songs -= 1

            fileList = glob.glob(f'/Users/martin/Desktop/{self.fullname}*')
            for filePath in fileList:
                try:
                    os.remove(filePath)
                    if verbose:
                        print(f'Deleted {filePath}\n')

                except:
                    print("Error while deleting file : ", filePath)

        
        else:
            self.downloaded = True
            with config.downloaded_songs_lock:
                config.downloaded_songs += 1
                
                if config.downloaded_songs < song_list_len:
                    print(  "\"" + self.name + "\" downloaded. [" + str(config.downloaded_songs) + "/" + str(song_list_len) + "]" + " songs downloaded....")
                else:
                    print("\"" + self.name + "\" downloaded. Finished downloading " + str(song_list_len) + " songs")
            # self.add_metadata()
        
    def add_metadata(self):
        print("Adding metadata to \"" + self.fullname + "\"")
        #* Add album cover
        try:
            cover_img = urlopen(self.metadata['cover_url'])
        except:
            print("ERROR: Could NOT get album cover for \"" + self.fullname + "\"")
        
        audio = EasyMP3(self.fullpath, ID3=ID3)

        try:
            audio.add_tags()
        except _util.error:
            print("ERROR: Could NOT \"add_tags()\" for \"" + self.fullname + "\"")
        
        audio.tags.add(
            APIC(
                encoding=3,  # UTF-8
                mime='image/png',
                type=3,  # 3 is for album art
                desc='Cover',
                data=cover_img.read()  # Reads and adds album art
            )
        )
        audio.save()
        
        print("Added album cover to \""+self.fullname+"\"")

        #* Add album info
        tags = EasyMP3(self.fullpath)
        tags["album"] = self.metadata['album']
        tags.save()
        

import re

import youtube_dl

from core.music.MediaFile import MediaFile
from core.music.AbstractProvider import AbstractProvider

regex = re.compile(r"^(.*)youtu[^/]+/(?:playlist\?list=|watch\?v=)?[a-zA-Z0-9-_]+[^/]")

ydl_options = {
    'format': 'bestaudio/best',
    'ignoreerrors': True,
    'quiet': True,
    'extract_flat': True
}
ydl = youtube_dl.YoutubeDL(ydl_options)


class YoutubeProvider(AbstractProvider):

    def accepts(self, url):
        return regex.match(url)

    def get_songs(self, url):
        with ydl:
            # Get song/playlist info
            result = ydl.extract_info(url, download=False)

            # Create common array of results, same structure for both single videos and playlists
            entries = result['entries'] if 'entries' in result else [result]

            medialist = []
            for entry in entries:
                media = MediaFile()

                # Set used provider to refer to it later
                media.provider = self

                # Set url to access this media on the website
                # media.stream_url will be requested before playing.
                media.web_url = entry['url']

                # Set various metadata
                media.duration = entry['duration'] if 'duration' in entry else None
                media.title = entry['title'] if 'title' in entry else None
                media.artist = entry['artist'] if 'artist' in entry else None
                media.thumbnail_url = entry['thumbnail'] if 'thumbnail' in entry else None

                medialist.append(media)

            return medialist

    def search(self, search_term):
        pass

    async def request_stream_url(self, song):
        with ydl:
            result = ydl.extract_info(song.web_url, download=False)

            print(result['url'])

            return result['url']
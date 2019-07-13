import re

from core.music.AbstractProvider import AbstractProvider

regex = re.compile(r"^(.*)\.(mp3|flac|wav|ogg|mp4|flv)$")


class DirectProvider(AbstractProvider):

    def accepts(self, url):
        return regex.match(url)

    def get_songs(self, url):
        pass

    def search(self, search_term):
        pass

    async def request_stream_url(self, song):
        pass

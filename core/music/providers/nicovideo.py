import re

from core.music.AbstractProvider import AbstractProvider

regex = re.compile(r"^(.*)nicovideo[^/]+/watch/([a-zA-Z0-9-_]+)")


class NicovideoProvider(AbstractProvider):

    def accepts(self, url):
        return regex.match(url)

    def get_songs(self, url):
        pass

    def search(self, search_term):
        pass

    async def request_stream_url(self, song):
        pass

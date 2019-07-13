from abc import ABC, abstractmethod

class AbstractProvider(ABC):

    @abstractmethod
    def accepts(self, url):
        """ Returns true if the url given is part of this provider, otherwise false.
            This should usually regex match the link for common url patterns.
        """

    @abstractmethod
    def get_songs(self, url):
        """ Analyses the url and retrieves the appropriate Song information
            Can either return one MediaFile object or an array of them.
        """

    @abstractmethod
    def search(self, search_term):
        """ Search the provider for the term given and retrieves a list of
            MediaFile objects as search results
        """

    @abstractmethod
    async def request_stream_url(self, song):
        """ Request a new stream url to the song given.
            This happens right before the song begins to play, so that the newest possible
            stream url is used.

            If this particular provider doesn't use expiring urls,
            set stream_url of the song in get_songs and search already.
            Then just pass this implementation.
        """
        pass
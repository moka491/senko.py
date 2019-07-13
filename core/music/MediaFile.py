from dataclasses import dataclass

from core.music.AbstractProvider import AbstractProvider


@dataclass
class MediaFile:
    # the url where this media file can be found
    web_url: str = None

    # the final url used to play this file
    stream_url: str = None

    # name of the provider that provided this file
    provider: AbstractProvider = None

    # if set, this is the name of the already downloaded version
    download_file: str = None

    # duration of the song, in seconds
    duration: int = None

    # title of the song. Can either be title + artist separated, or a filename
    title = None
    artist = None

    # url to the thumbnail, if one is available
    thumbnail_url = None
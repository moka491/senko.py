from dataclasses import dataclass

@dataclass
class Metadata:
    title = None
    artist = None
    duration = None

@dataclass
class Song:
    url: str
    download_file: str = None
    meta: Metadata = None
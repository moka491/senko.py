import asyncio
import atexit
import uuid
import os
import time
import ffmpeg
from discord import AudioSource
from discord.opus import Encoder as OpusEncoder
from core.music.Song import Song


class Source(AudioSource):
    ffmpeg = None

    song = None
    file = None
    filename = None

    def __init__(self, song: Song):
        self.song = song

        if song.download_file is not None:
            # Set previously used filename
            self.filename = song.download_file
        else:
            # Create random file for song stream
            self.filename = "tmp/" + str(uuid.uuid4())

            # Create ffmpeg instance to write to this file
            self.ffmpeg = (
                ffmpeg
                    .input(song.url)
                    .output(self.filename, format='s16le', ac=2, ar='48k')
                    .run_async(overwrite_output=True)
            )

    async def download_started(self):
        print(self.song)

        # async wait for file to be created by ffmpeg
        while not os.path.exists(self.filename):
            await asyncio.sleep(0.2)

        # Open file for reading
        self.file = open(self.filename, 'rb')

        # Store filename in song so that next time, it doesn't have to be downloaded
        self.song.download_file = self.filename

        print("file written!")

    def read(self):
        ret = self.file.read(OpusEncoder.FRAME_SIZE)
        if len(ret) != OpusEncoder.FRAME_SIZE:
            print(len(ret))
            return b''

        return ret

    @atexit.register
    def cleanup(self):
        print("cleanup!")
        if self.ffmpeg is not None:
            self.ffmpeg.wait()

import asyncio
import atexit
import uuid
import os
import time
import ffmpeg
from discord import AudioSource
from discord.opus import Encoder as OpusEncoder

class Player(AudioSource):

    file = None
    song = None
    filename = None

    def __init__(self, song):
        self.song = song

        # Create random file for song stream
        self.filename = str(uuid.uuid4())

        # Create ffmpeg instance to write to this file
        self.ffmpeg = (
            ffmpeg
                .input(song)
                .output(self.filename, format='s16le', ac=2, ar='48k')
                .run_async(quiet=True, overwrite_output=True)
        )

    async def await_download(self):
        while not os.path.exists(self.filename):
            await asyncio.sleep(0.5)
        self.file = open(self.filename, 'rb')


    def read(self):
        ret = self.file.read(OpusEncoder.FRAME_SIZE)
        if len(ret) != OpusEncoder.FRAME_SIZE:
            return b''

        return ret

    @atexit.register
    def cleanup(self):
        if self.ffmpeg:
            self.ffmpeg.stdout.close()
            self.ffmpeg.wait()

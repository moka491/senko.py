import asyncio
import atexit
import subprocess
import uuid
import os
from asyncio.subprocess import PIPE, STDOUT

from discord import AudioSource
from discord.opus import Encoder as OpusEncoder
from core.music.MediaFile import MediaFile
import config

class Source(AudioSource):
    command_line = "ffmpeg -y -i '{}' -f s16le -ac 2 -ar 48000 {} 2>&1 | grep Duration " #\
                   #"| sed 's/Duration: \(.*\), start/\1/g'"

    ffmpeg = None

    song = None
    file = None
    filename = None

    def __init__(self, song: MediaFile):
        self.song = song

    async def prepare(self):

        if self.song.download_file is not None:
            # Set previously used filename
            self.filename = self.song.download_file
        else:
            # Create random file for song stream
            self.filename = "tmp/" + str(uuid.uuid4())

            # If a stream url is set inside the media file, use it. Otherwise request a fresh stream url
            stream_url = self.song.stream_url or await self.song.provider.request_stream_url(self.song)

            print(stream_url)

            # Create ffmpeg instance to write to this file
            self.ffmpeg = subprocess.Popen(self.command_line.format(stream_url, self.filename), shell=True)

        num_tries = 0
        num_tries_allowed = config.download_wait_time * 5

        # async wait for file to be created by ffmpeg
        while not os.path.exists(self.filename):

            # If number of checks has passed config value, return false to stop waiting
            num_tries += 1
            if (num_tries) > num_tries_allowed:
                return False

            # Await next check in .2 seconds
            await asyncio.sleep(0.2)

        # Open file for reading
        self.file = open(self.filename, 'rb')

        # Store filename in song so that next time, it doesn't have to be downloaded
        self.song.download_file = self.filename

        # Return true for successful file check
        return True

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

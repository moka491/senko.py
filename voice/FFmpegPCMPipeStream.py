import asyncio

import aiohttp, ffmpeg
from discord import AudioSource
from discord.opus import Encoder as OpusEncoder


class FFmpegPCMPipeStream(AudioSource):

    def __init__(self, source, bot):
        self.source = source
        self.process = None
        self.bot = bot

        try:
            self.process = (
                ffmpeg
                .input('pipe:', stimeout=10000)
                .output('pipe:', format='s16le', ac=2, ar='48k')
                .run_async(pipe_stdin=True, pipe_stdout=True)
            )
            self.bot.loop.create_task(self.stream_file(source))

        except Exception:  # todo
            pass

    async def stream_file(self, source):
        async with aiohttp.ClientSession() as session:
            async with session.get(source) as response:
                async for data in response.content.iter_any():
                    self.process.stdin.write(data)

    def read(self):
        ret = self.process.stdout.read(OpusEncoder.FRAME_SIZE)
        if len(ret) != OpusEncoder.FRAME_SIZE:
            return b''
        return ret

    def cleanup(self):
        print("cleanup")
        if hasattr(self, 'process'):
            proc = self.process
            if proc is None:
                return

            proc.kill()
            if proc.poll() is None:
                proc.communicate()
            else:
                self.process = None
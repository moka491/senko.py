import asyncio

import aiohttp, ffmpeg
from discord import AudioSource
from discord.opus import Encoder as OpusEncoder


class FFmpegPCMPipeStream(AudioSource):

    def __init__(self, source, bot):
        self.source = source
        self.bot = bot

        self.ffmpeg = None
        self.streamtask = None

        try:
            self.ffmpeg = (
                ffmpeg
                .input('pipe:')
                .output('pipe:', format='s16le', ac=2, ar='48k')
                .run_async(pipe_stdin=True, pipe_stdout=True)
            )
            self.streamtask = self.bot.loop.create_task(self.stream_file(source))

        except Exception:  # todo
            pass

    async def stream_file(self, source):
        async with aiohttp.ClientSession() as session:
            async with session.get(source) as response:
                async for data in response.content.iter_any():
                    self.ffmpeg.stdin.write(data)

    def read(self):
        ret = self.ffmpeg.stdout.read(OpusEncoder.FRAME_SIZE)
        if len(ret) != OpusEncoder.FRAME_SIZE:
            return b''
        return ret

    def cleanup(self):
        print("cleanup")
        if hasattr(self, 'process'):
            proc = self.ffmpeg
            if proc is None:
                return

            proc.kill()
            if proc.poll() is None:
                proc.communicate()
            else:
                self.ffmpeg = None

    def stop(self):
        if self.streamtask is not None:
            self.streamtask.cancel()

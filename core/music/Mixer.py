import audioop
from discord import AudioSource
from discord.opus import Encoder as OpusEncoder

class Mixer(AudioSource):
    source = None
    new_source = None
    fade_cur = 0.0
    fade_time = 2.0

    def set_source(self, source):
        self.source = source

    def get_source(self):
        return self.source

    def crossfade_to(self, source):
        self.new_source = source

    def read(self):
        # If fading but fadeTime is over, finish fading process
        if self.fade_cur > self.fade_time:
            self.source = self.new_source
            self.new_source = None
            self.fade_cur = 0.0

        # If not fading, or fading ended, read from the current source
        if not self.new_source:
            return self.source.read()

        # Else, for fading, update time
        self.fade_cur += (OpusEncoder.FRAME_LENGTH / 1000)

        # Calculate volumes for both sources (0 <= x <= 1)
        vol_new = self.fade_cur / self.fade_time
        vol_cur = 1 - vol_new

        # Apply volumes
        segment_cur = audioop.mul(self.source.read(), 2, vol_cur)
        segment_new = audioop.mul(self.new_source.read(), 2, vol_new)

        # Return sum of both segments
        return audioop.add(segment_cur, segment_new, 2)
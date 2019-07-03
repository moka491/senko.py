import audioop
from discord import AudioSource
from discord.opus import Encoder as OpusEncoder

class Mixer(AudioSource):
    player = None
    newPlayer = None
    fadeCur = 0.0
    fadeTime = 3.0

    def setPlayer(self, player):
        self.player = player

    def getPlayer(self):
        return self.player

    def crossfadeTo(self, player):
        self.newPlayer = player

    def read(self):
        # If fading but fadeTime is over, finish fading process
        if self.fadeCur > self.fadeTime:
            self.player = self.newPlayer
            self.newPlayer = None
            self.fadeCur = 0.0

        # If not fading, or fading ended, read from the current player
        if not self.newPlayer:
            return self.player.read()

        # Else, for fading, update time
        self.fadeCur += (OpusEncoder.FRAME_LENGTH / 1000)

        # Calculate volumes for both players (0 <= x <= 1)
        volNew = self.fadeCur / self.fadeTime
        volCur = 1 - volNew

        # Apply volumes
        segmentCur = audioop.mul(self.player.read(), 2, volCur)
        segmentNew = audioop.mul(self.newPlayer.read(), 2, volNew)

        # Return sum of both segments
        return audioop.add(segmentCur, segmentNew, 2)
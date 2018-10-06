# Copyright (C) 2018, Uri Shaked. MIT License.

import board
import digitalio
import time
from vs1053 import Player
from softspi import SoftSPI

r = digitalio.DigitalInOut(board.LED2_R)
r.switch_to_output(False)
r.value = False

print ("Init!")

spi = SoftSPI(board.P0_22, MISO=board.P0_20, MOSI=board.P1_00)
player = Player(
    spi,
    xResetPin = board.P1_10,
    dReqPin = board.P1_13,
    xDCSPin = board.P1_15,
    xCSPin = board.P0_02,
    CSPin = board.P0_24
)
player.setVolume(1.0)

print ("Play!")

inputFile = open('promo.mp3', mode='rb')
startTime = time.monotonic()
buf = bytearray(32)
while inputFile.readinto(buf):
    player.writeData(buf)
print("Total time:", time.monotonic() - startTime)

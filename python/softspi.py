# Accelerated Software SPI Implementation for CircuitPython.
# Copyright (C) 2018, Uri Shaked. MIT License.
# This implementation only implements sending data, and assumes we are running
# on nRF52840, with SCLK connected to P0_22 and MOSI to P1_00.

import digitalio

class SoftSPI:
    def __init__(self, clk, MOSI, MISO):
        self.clk = digitalio.DigitalInOut(clk)
        self.clk.direction = digitalio.Direction.OUTPUT
        self.MOSI = digitalio.DigitalInOut(MOSI)
        self.MOSI.direction = digitalio.Direction.OUTPUT
        self.MISO = digitalio.DigitalInOut(MISO)
        self.MISO.direction = digitalio.Direction.INPUT
    
    def configure(self, baudrate=500000, polarity=0):
        pass
    
    def try_lock(self):
        return True
        
    def unlock(self):
        pass
        
    def write(self, data):
        @micropython.viper
        def sendByte(b: int):
            gpio0_set = ptr32(0x50000508)
            gpio0_clr = ptr32(0x5000050c)
            gpio1_set = ptr32(0x50000808)
            gpio1_clr = ptr32(0x5000080c)
            clk = 1 << 22
            mosi = 1 << 0
            for i in range(7, -1, -1):  # [7 to 0]
                gpio0_clr[0] = clk      # Clock Low
                if b & (1 << i):
                    gpio1_set[0] = mosi
                else:
                    gpio1_clr[0] = mosi
                gpio0_set[0] = clk      # Clock High

        for b in data:
            sendByte(b)
    
    def write_readinto(self, data, target):
        self.write(data)

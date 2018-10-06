from ubluepy import Service, Characteristic, UUID, Peripheral, constants
from board import LED1, LED2_B
import digitalio
import time

led_conn = digitalio.DigitalInOut(LED2_B)
led_conn.direction = digitalio.Direction.OUTPUT
led_conn.value = True

led_data = digitalio.DigitalInOut(LED1)
led_data.direction = digitalio.Direction.OUTPUT
led_data.value = True

def setPlayer(p):
    global player
    player = p

def eventHandler(id, handle, data):
    if id == constants.EVT_GAP_CONNECTED:
        led_conn.value = False
        print("--> Connected!")
    elif id == constants.EVT_GAP_DISCONNECTED:
        led_conn.value = True
        print("<-- Disconnected.")
    elif id == constants.EVT_GATTS_WRITE:
        if player:
            led_data.value = False
            for i in range(0, len(data), 32):
                player.writeData(data[i:i+32])
            led_data.value = True
        else:
            print("Got data, but no player is set")

service = Service(UUID(0xfefe))
soundChar = Characteristic(UUID(0xfe01), props = Characteristic.PROP_WRITE | Characteristic.PROP_WRITE_WO_RESP)
service.addCharacteristic(soundChar)
p = Peripheral()
p.addService(service)
p.setConnectionHandler(eventHandler)
p.advertise(device_name="Badge", services=[service])

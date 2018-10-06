// Send file to CircuitPython over BLE. Edit the following constants to customize
// the serial port of your nRF dongle, the Bluetooth device of the target address, 
// or the name of the file to transmit:

const PORT = 'COM16';
const TARGET_DEVICE_ADDR = 'F3:A7:50:50:1B:0F';
const FILE_TO_SEND = 'promo-full.mp3';

const ble = require('pc-ble-driver-js');
const doAsync = require('doasync');
const fs = require('fs');

const apiVersion = 'v3';
const MTU = 247;

async function openAdapter(adapter) {
  const baudRate = process.platform === 'darwin' ? 115200 : 1000000;
  console.log(
    `Opening adapter with ID: ${
      adapter.instanceId
    } and baud rate: ${baudRate}...`
  );

  await adapter.open({ baudRate, logLevel: 'error' });
}

async function main() {
  const adapterFactory = ble.AdapterFactory.getInstance(undefined, {
    enablePolling: false
  });
  let adapter = doAsync(adapterFactory.createAdapter(apiVersion, PORT, ''));
  await openAdapter(adapter);

  console.log('Adapter opened!');
  const options = {
    scanParams: {
      active: false,
      interval: 100,
      window: 50,
      timeout: 20
    },
    connParams: {
      min_conn_interval: 7.5,
      max_conn_interval: 7.5,
      slave_latency: 0,
      conn_sup_timeout: 4000
    }
  };
  await adapter.connect(
    TARGET_DEVICE_ADDR,
    options
  );
  const devs = await adapter.getDevices();
  const device = devs[Object.keys(devs)[0]];
  try {
    console.log('Connected!', device.name);
    const actualMTU = await await adapter.requestAttMtu(device.instanceId, MTU);
    console.log('MTU:', actualMTU);

    const services = await adapter.getServices(device.instanceId);
    const serviceFEFE = services.find(s => s.uuid === 'FEFE');
    console.log('Found service!', serviceFEFE.instanceId);
    const characteristics = await adapter.getCharacteristics(
      serviceFEFE.instanceId
    );
    
    const characteristicFE01 = characteristics.find(c => c.uuid === 'FE01');
    console.log('Found characteristic!', characteristicFE01.instanceId);
    const fd = fs.openSync(FILE_TO_SEND, 'r');
    buffer = new Uint8Array(actualMTU - 4);

    console.log('Sending file...');
    while (fs.readSync(fd, buffer, 0, buffer.length)) {
      await adapter.writeCharacteristicValue(
        characteristicFE01.instanceId,
        Array.from(buffer),
        false
      );
    }

    console.log('Done !');
  } finally {
    await adapter.disconnect(device.instanceId);
    await adapter.close();
  }
}

main();

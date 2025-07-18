import bluetooth
from ble_advertising import advertising_payload
from ble_stream import BLEStream
from micropython import const
import os

# Realtime start
from vl53l1x import VL53L0X
from am2320 import AM2320
from machine import reset, Pin, SoftI2C
# from declare_button import button_debounce
# Realtime import end

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)

_UART_UUID = bluetooth.UUID(0x8000)
_UART_TX = (bluetooth.UUID(0x8001), bluetooth.FLAG_NOTIFY,)
_UART_RX = (bluetooth.UUID(0x8002),bluetooth.FLAG_WRITE,)
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX),)

REPL_UUID = bluetooth.UUID(0x180D)
REPL_TX = (bluetooth.UUID(0x2A37), bluetooth.FLAG_NOTIFY,)
REPL_RX = (bluetooth.UUID(0x2A38),bluetooth.FLAG_WRITE,)
REPL_SERVICE = (REPL_UUID, (REPL_TX, REPL_RX,),)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)


class BLEUART:
    def __init__(self, name="esp32", rxbuf=512):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        services = (REPL_SERVICE, _UART_SERVICE)
        ((self.repl_tx, self.repl_rx), (self._tx_handle, self._rx_handle)) = self._ble.gatts_register_services(services)
        
        # Increase the size of the rx buffer and enable append mode.
        # self._ble.gatts_set_buffer(self._rx_handle, rxbuf, True)
        self._ble.gatts_set_buffer(self.repl_rx, rxbuf, True)
        self._connections = set()
        self.repl_rx_buffer = bytearray()
        self._handler = None
        self._tmp_file_upload = 'new_code_uploaded.py'
        
        # Optionally add services=[_UART_UUID], but this is likely to make the payload too large.
        self._payload = advertising_payload(
            name=name,
            services=[_UART_UUID, REPL_UUID]
        )
        self._advertise()

    def irq(self, handler):
        self._handler = handler

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            open(self._tmp_file_upload, 'w').close();
            
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            
            if conn_handle in self._connections and value_handle == self.repl_rx:
                # Handle RELP
                self.repl_rx_buffer += self._ble.gatts_read(self.repl_rx)
                if self._handler:
                    self._handler()
                
            if conn_handle in self._connections and value_handle == self._rx_handle:
                # Handle Upload code
                write_type = self._ble.gatts_read(self._rx_handle).decode("utf-8")
                
                # Handle sensor read
                if write_type == "__read__distance_":
                    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
                    tof = VL53L0X(i2c)
                    tof.start()
                    tof.stop()
                    distance=tof.read()
                    distance = write_type + str(distance)
                    self._ble.gatts_notify(conn_handle, self._tx_handle, distance)
                    return
                
                if write_type == "__read__temperature_":
                    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
                    sensor = AM2320(i2c)
                    sensor.measure()
                    temperature = sensor.temperature()
                    temperature = write_type + str(temperature)
                    self._ble.gatts_notify(conn_handle, self._tx_handle, temperature)
                    return
                
                if write_type == "__read__humidity_":
                    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
                    sensor = AM2320(i2c)
                    sensor.measure()
                    humidity = sensor.humidity()
                    humidity = write_type + str(humidity)
                    self._ble.gatts_notify(conn_handle, self._tx_handle, humidity)
                    return
                
                if write_type.startswith("__read__button"):
                    value = button_debounce(int(write_type[14]))
                    button_value = write_type + str(value)
                    self._ble.gatts_notify(conn_handle, self._tx_handle, button_value)
                    return
                
                if write_type == "__read__acceleration_":
                    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
                    accel_address = 0x19  
                    mag_address = 0x1E
                    i2c.writeto_mem(accel_address, 0x20, bytes([0x27]))  # CTRL_REG1_A: Turn on accelerometer, enable all axes
                    i2c.writeto_mem(mag_address, 0x00, bytes([0x14]))    # CRA_REG_M: Set data output rate (30 Hz), continuous conversion mode
                    i2c.writeto_mem(mag_address, 0x01, bytes([0x20]))    # CRB_REG_M: Set scale to +/- 1.3 Gauss
                    data = i2c.readfrom_mem(accel_address, 0x28 | 0x80, 6)
                    x = (data[1] << 8) | data[0]
                    y = (data[3] << 8) | data[2]
                    z = (data[5] << 8) | data[4]
                    x = x / 256
                    y = y / 256
                    z = z / 256
                    str_value = write_type + str(x) + "_" + str(y) + "_" + str(z)
                    self._ble.gatts_notify(conn_handle, self._tx_handle, str_value)
                    return
                
                if write_type == "__read__compass_":
                    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
                    accel_address = 0x19  
                    mag_address = 0x1E
                    i2c.writeto_mem(accel_address, 0x20, bytes([0x27]))  # CTRL_REG1_A: Turn on accelerometer, enable all axes
                    i2c.writeto_mem(mag_address, 0x00, bytes([0x14]))    # CRA_REG_M: Set data output rate (30 Hz), continuous conversion mode
                    i2c.writeto_mem(mag_address, 0x01, bytes([0x20]))    # CRB_REG_M: Set scale to +/- 1.3 Gauss
                    data = i2c.readfrom_mem(mag_address, 0x03 | 0x80, 6)
                    x = (data[0] << 8) | data[1]
                    y = (data[4] << 8) | data[5]
                    z = (data[2] << 8) | data[3]
                    x = x / 256
                    y = y / 256
                    z = z / 256
                    str_value = write_type + str(x) + "_" + str(y) + "_" + str(z)
                    self._ble.gatts_notify(conn_handle, self._tx_handle, str_value)
                    return

                # Handle Upload_code
                if write_type == "__done__":
                    os.rename(self._tmp_file_upload, 'main.py')
                    # Hard reset
                    reset()
                    return
                with open(self._tmp_file_upload, 'a') as file:
                    # append chunks
                    file.write(write_type)
                # Notify to write next chunk
                self._ble.gatts_notify(conn_handle, self._tx_handle, "bounce back")
    
    def any(self):        
        return len(self.repl_rx_buffer)

    def read(self, sz=None):
        if not sz:
            sz = len(self.repl_rx_buffer)
        result = self.repl_rx_buffer[0:sz]
        self.repl_rx_buffer = self.repl_rx_buffer[sz:]
        return result

    def write(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self.repl_tx, data)

    def close(self):
        for conn_handle in self._connections:
            self._ble.gap_disconnect(conn_handle)
        self._connections.clear()

    def _advertise(self, interval_us=100):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
        
def start(name):
    ble = BLEUART(name=name)
    os.dupterm(BLEStream(ble))


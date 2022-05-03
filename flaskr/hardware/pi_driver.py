import pigpio
import atexit


class PiDriver:
    _rpi_bcm_pin = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
    ]
    _port_modes = {0: "INPUT", 1: "OUTPUT", 2: "ALT5", 3: "ALT4", 4: "ALT0", 5: "ALT1", 6: "ALT2", 7: "ALT3"}
    _port_function = {
        0: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "AVEIN VCLK", 4: "I2C0 SDA", 5: "SMI SA5", 6: "DPI CLK",
            7: "AVEOUT VCLK"},
        1: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "AVEIN DSYNC", 4: "I2C0 SCL", 5: "SMI SA4", 6: "DPI DEN",
            7: "AVEOUT DSYNC"},
        2: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "AVEIN VSYNC", 4: "I2C1 SDA", 5: "SMI SA3", 6: "DPI VSYNC",
            7: "AVEOUT VSYNC"},
        3: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "AVEIN HSYNC", 4: "I2C1 SCL", 5: "SMI SA2", 6: "DPI HSYNC",
            7: "AVEOUT HSYNC"},
        4: {0: "INPUT", 1: "OUTPUT", 2: "JTAG TDI", 3: "AVEIN VID0", 4: "GPCLK0", 5: "SMI SA1", 6: "DPI D0",
            7: "AVEOUT VID0"},
        5: {0: "INPUT", 1: "OUTPUT", 2: "JTAG TDO", 3: "AVEIN VID1", 4: "GPCLK1", 5: "SMI SA0", 6: "DPI D1",
            7: "AVEOUT VID1"},
        6: {0: "INPUT", 1: "OUTPUT", 2: "JTAG RTCK", 3: "AVEIN VID2", 4: "GPCLK2", 5: "SMI SOE_N / SE", 6: "DPI D2",
            7: "AVEOUT VID2"},
        7: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "AVEIN VID3", 4: "SPI0 CE1", 5: "SMI SWE_N / SRW_N", 6: "DPI D3",
            7: "AVEOUT VID3"},
        8: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "AVEIN VID4", 4: "SPI0 CE0", 5: "SMI SD0", 6: "DPI D4",
            7: "AVEOUT VID4"},
        9: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "AVEIN VID5", 4: "SPI0 MISO", 5: "SMI SD1", 6: "DPI D5",
            7: "AVEOUT VID5"},
        10: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "AVEIN VID6", 4: "SPI0 MOSI", 5: "SMI SD2", 6: "DPI D6",
             7: "AVEOUT VID6"},
        11: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "AVEIN VID7", 4: "SPI0 SCLK", 5: "SMI SD3", 6: "DPI D7",
             7: "AVEOUT VID7"},
        12: {0: "INPUT", 1: "OUTPUT", 2: "JTAG TMS", 3: "AVEIN VID8", 4: "PWM0", 5: "SMI SD4", 6: "DPI D8",
             7: "AVEOUT VID8"},
        13: {0: "INPUT", 1: "OUTPUT", 2: "JTAG TCK", 3: "AVEIN VID9", 4: "PWM1", 5: "SMI SD5", 6: "DPI D9",
             7: "AVEOUT VID9"},
        14: {0: "INPUT", 1: "OUTPUT", 2: "UART1 TXD", 3: "AVEIN VID10", 4: "UART0 TXD", 5: "SMI SD6", 6: "DSI D10",
             7: "AVEOUT VID10"},
        15: {0: "INPUT", 1: "OUTPUT", 2: "UART1 RXD", 3: "AVEIN VID11", 4: "UART0 RXD", 5: "SMI SD7", 6: "DPI D11",
             7: "AVEOUT VID11"},
        16: {0: "INPUT", 1: "OUTPUT", 2: "UART1 CTS", 3: "SPI1 CE2", 4: "FL0", 5: "SMI SD8", 6: "DPI D12",
             7: "UART0 CTS"},
        17: {0: "INPUT", 1: "OUTPUT", 2: "UART1 RTS", 3: "SPI1 CE1", 4: "FL1", 5: "SMI SD9", 6: "DPI D13",
             7: "UART0 RTS"},
        18: {0: "INPUT", 1: "OUTPUT", 2: "PWM0", 3: "SPI1 CE0", 4: "PCM CLK", 5: "SMI SD10", 6: "DPI D14",
             7: "I2CSL SDA / MOSI"},
        19: {0: "INPUT", 1: "OUTPUT", 2: "PWM1", 3: "SPI1 MISO", 4: "PCM FS", 5: "SMI SD11", 6: "DPI D15",
             7: "I2CSL SCL / SCLK"},
        20: {0: "INPUT", 1: "OUTPUT", 2: "GPCLK0", 3: "SPI1 MOSI", 4: "PCM DIN", 5: "SMI SD12", 6: "DPI D16",
             7: "I2CSL MISO"},
        21: {0: "INPUT", 1: "OUTPUT", 2: "GPCLK1", 3: "SPI1 SCLK", 4: "PCM DOUT", 5: "SMI SD13", 6: "DPI D17",
             7: "I2CSL CE"},
        22: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "JTAG TRST", 4: "SD0 CLK", 5: "SMI SD14", 6: "DPI D18", 7: "SD1 CLK"},
        23: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "JTAG RTCK", 4: "SD0 CMD", 5: "SMI SD15", 6: "DPI D19", 7: "SD1 CMD"},
        24: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "JTAG TDO", 4: "SD0 DAT0", 5: "SMI SD16", 6: "DPI D20", 7: "SD1 DAT0"},
        25: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "JTAG TCK", 4: "SD0 DAT1", 5: "SMI SD17", 6: "DPI D21", 7: "SD1 DAT1"},
        26: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "JTAG TDI", 4: "SD0 DAT2", 5: "TE0", 6: "DPI D22", 7: "SD1 DAT2"},
        27: {0: "INPUT", 1: "OUTPUT", 2: "", 3: "JTAG TMS", 4: "SD0 DAT3", 5: "TE1", 6: "DPI D23", 7: "SD1 DAT3"}
    }
    _port_groups = {
        'GPIO': _rpi_bcm_pin,
        'SPI0': [7, 8, 9, 10, 11],
        'SPI1': [16, 17, 18, 19, 20, 21],
        'I2C0': [0, 1],
        'IC21': [2, 3],
        'UART': [14, 15, 16, 17],
        'PCM': [18, 19, 20, 21],
        'PWM0': [12, 18],
        'PWM1': [13, 19]
    }
    _port_assignment = {}
    _temp_sens_prefix = {'10': 'DS18S20', '22': 'DS1822', '28': 'DS18B20', '41': 'DS28EA00', '3B': 'DS1825'}
    _pwm_freq = 25000
    _pwm_divider = 10000
    _callback_handles = {}
    _pi = None
    _w1_path = "/sys/bus/w1/devices/"

    def __init__(self, app=None):
        self.app = None
        self._pi = pigpio.pi()

        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        atexit.register(self.shutdown)

        for i in self._rpi_bcm_pin:
            if str(self._port_function[i][self._pi.get_mode(i)]) == "INPUT":
                self._port_assignment[i] = {'type': str(self._port_function[i][self._pi.get_mode(i)]), 'use': False}
            else:
                self._port_assignment[i] = {'type': str(self._port_function[i][self._pi.get_mode(i)]), 'use': True}

        file_arr = self.__read_file("/boot/config.txt", 1024).split('\n')

        for i in file_arr:
            if i.startswith('dtoverlay') and 'w1-gpio' in i:
                if 'gpiopin' in i:
                    temp = i.split("gpiopin")[1].split("=")[1]
                    self._port_assignment[int(temp)] = {'type': "1W", 'use': True}
                else:
                    self._port_assignment[4] = {'type': "1W", 'use': True}

    def shutdown(self):
        self._pi.stop()

    def __read_file(self, path, read_length=6):
        content = ""

        handle = self._pi.file_open(path, pigpio.FILE_READ)
        done = False

        while not done:
            e, f = self._pi.file_read(handle, read_length)
            if e > 0:
                content += f.decode()[:-1]
            else:
                done = True

        self._pi.file_close(handle)

        return content

    def get_ports(self):
        return self._port_assignment

    def get_pwm_channel_pins(self):
        return {0: self._port_groups['PWM0'], 1: self._port_groups['PWM1']}

    def list_w1_sensors(self):
        sensor_list = []

        for i in self._temp_sens_prefix:
            c, d = self._pi.file_list(self._w1_path + i + "*")
            if c > 0:
                for k in d.decode()[:-1].split('\n'):
                    sensor_list.append(
                        dict(
                            id=k.split('/')[5],
                            type=self._temp_sens_prefix[i],
                            value=int(self.__read_file(k + "temperature"))
                        )
                    )

        return sensor_list

    def get_w1_temp(self, sens_id):
        return int(self.__read_file(self._w1_path + sens_id + "/temperature"))

    def __set_pwm(self, pin, duty):
        self._pi.hardware_PWM(pin, self._pwm_freq, duty)

    def init_pwm(self, pin):
        if pin in self._port_groups['PWM0'] and self._port_assignment[pin]['type'] != 'PWM0':
            self._port_assignment[pin] = {'type': 'PWM0', 'use': True}
        elif pin in self._port_groups['PWM1'] and self._port_assignment[pin]['type'] != 'PWM1':
            self._port_assignment[pin] = {'type': 'PWM1', 'use': True}
        else:
            return

        self.__set_pwm(pin, 0)

    def set_duty(self, pin, duty):
        if self._port_assignment[pin]['type'] == 'PWM0' or self._port_assignment[pin]['type'] == 'PWM1':
            self.__set_pwm(pin, (100 - duty) * self._pwm_divider)

    def get_duty(self, pin):
        return 100 - (self._pi.get_PWM_dutycycle(pin) / self._pwm_divider)

    def init_input(self, pin, pull='UP'):
        if not self._port_assignment[pin]['use']:
            self._pi.set_mode(pin, pigpio.INPUT)

            if pull == 'UP':
                self._pi.set_pull_up_down(pin, pigpio.PUD_UP)
            elif pull == 'DOWN':
                self._pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
            elif pull == 'OFF':
                self._pi.set_pull_up_down(pin, pigpio.PUD_OFF)
            else:
                return

            self._port_assignment[pin] = {'type': 'INPUT', 'use': True}

    def init_input_callback(self, pin, edge='RISING'):
        if edge == 'BOTH':
            self._callback_handles[pin] = self._pi.callback(pin, pigpio.EITHER_EDGE)
        elif edge == 'RISING':
            self._callback_handles[pin] = self._pi.callback(pin, pigpio.RISING_EDGE)
        elif edge == 'FALLING':
            self._callback_handles[pin] = self._pi.callback(pin, pigpio.FALLING_EDGE)

    def get_input_counter(self, pin):
        if pin in self._callback_handles:
            count = self._callback_handles[pin].tally()
            self._callback_handles[pin].reset_tally()

            return count

        return None

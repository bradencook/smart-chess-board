import serial
from serial.tools.list_ports import comports


class Talker:
    TERMINATOR = '\r'.encode('UTF8')

    def __init__(self, timeout=1):
        # Detect the serial port
        port = self.find_serial_port()
        if not port:
            print("No suitable serial port found!")
            exit()
        self.serial = serial.Serial(port, 115200, timeout=timeout)

    def find_serial_port(self):
        ports = comports()
        for port in ports:
            if "Board in FS mode" in port.description:
                return port.device
        return None


    def send(self, text: str):
        line = '%s\r\f' % text
        self.serial.write(line.encode('utf-8'))
        reply = self.receive()
        reply = reply.replace('>>> ','') # lines after first will be prefixed by a propmt
        if reply != text: # the line should be echoed, so the result should match
            raise ValueError('expected %s got %s' % (text, reply))

    def receive(self) -> str:
        line = self.serial.read_until(self.TERMINATOR)
        return line.decode('UTF8').strip()

    def close(self):
        self.serial.close()

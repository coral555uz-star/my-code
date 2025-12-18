import serial

class UDSClient:
    def __init__(self,port,baudrate):
        self.ser = serial.Serial(port, baudrate)

    def close(self):
        self.ser.close()
    
    def send(self, data):
        self.ser.write(data)
    
    def receive(self):
        return self.ser.read(100)  # Read up to 100 bytes
    
    def read_data(identifier):
        request = bytearray([0x22,identifier])

        self.send(request)

        response = self.receive()

        return response


if __name__ == "__main__":
    client=UDSClient(port='COM1',baudrate=9600)

    try:
        data=client.read_data(0x01)
        print("Received data:", data)
    finally:
        client.close()
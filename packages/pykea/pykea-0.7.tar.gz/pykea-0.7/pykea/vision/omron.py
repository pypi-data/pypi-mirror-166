import socket
from time import sleep

class Terminal():
    def __init__(self, host='192.168.0.10', port=9876, timeout=2) -> None:
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(timeout)
        self.connected = False
        self.connect()
                
    def connect(self) -> None:
        try:
            self.client.connect((self.host, self.port))
            print('client connected')
            self.connected = True
        except socket.error as e:
            print(f'Connection Error: {e}')
            self.connected = False
        
    def send(self, msg='M\r') -> None:
        try:
            self.client.sendall(msg.encode())
        except socket.timeout as e:
            print('Sending', e)

    def receive(self) -> str:
        data = None
        try:
            data = self.client.recv(2048)
        except socket.timeout as e:
            print('Receiving', e)
        return data

    def run(self):
        while self.connected:
            try:
                self.send()
                sleep(.1)
                data = self.receive()
                
                if data:
                    if data.decode().strip() == 'ER':
                        print('Camera Offline')
                    elif data.decode().strip() == 'OK':
                        print(f'Received data block 1: {data.decode().strip()}')
                        data = self.receive()
                        print(f'Received data block 2: {data.decode()}')
                inp = input('Press Enter to trigger the camera or q to quit >> ')
                if inp == 'q' or inp == 'Q':
                    self.client.close()
                    print('Client closed')
                    break
            except KeyboardInterrupt:
                self.client.close()
            except:
                print('connection Interrupted')
                break

        self.client.close()



# if __name__ == '__main__':
#     tester = Terminal()
#     tester.run()










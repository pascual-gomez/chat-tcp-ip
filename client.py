import socket
import threading

class TCPClient():
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

    def start_client(self):
        print("Starting client...")
        try:
            self.client_socket.connect((self.server_address, self.server_port))
            print(f"Connected to {self.server_address}")
            receive_thread = threading.Thread(target=self.receive_message, args=(self.client_socket, self.server_address))
            receive_thread.start()

            while True:
                message = input("Write a message:")
                self.client_socket.send(message.encode())

        except OSError:
            pass

    def receive_message(self, client_socket, server_address):
        print('Listening...')
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"{server_address}: {data.decode('utf-8')}")


def main():
    server_addr = '10.161.51.244'
    server_port = 80
    tcpClient = TCPClient(server_addr, server_port)
    tcpClient.start_client()

if __name__ == '__main__':
    main()

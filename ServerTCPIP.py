import socket
import pyaudio
import threading

p = pyaudio.PyAudio()
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

class  TCPService():
    def __init__(self, server_address, server_port):
        self.service_type = "tcp/ip"
        self.server_address = server_address
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((server_address, server_port))
        self.clients = []

    def accept_client_connection(self):
        print("Waiting for TCP/IP connection...")

        flag = True
        while flag == True:
            client, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client, addr))
            client_thread.start()
            self.clients.append(client_thread)
            if threading.active_count == 0:
                ans = input("There isn't active connections, stop listening?(y/n)\n")
                if ans == 'y':
                    flag = False


    def handle_client(self, client_socket, client_address):
        while True:
            try:
                audio = client_socket.recv(4096)
                if audio:
                    audio = client_socket.recv(4096)
                    stream.write(audio)
                    for c in self.clients:
                        if c != threading.current_thread():
                            c.client_socket.send(audio.encode())

            except:
                print(f"Client {client_address} disconnected, tcp/ip")
                # self.clients.remove(threading.current_thread())
                client_socket.close()
                return False

    def start_service(self):
        self.server_socket.listen(10)
        accept_thread = threading.Thread(target=self.accept_client_connection)
        accept_thread.start()


def main():
    server_addr = '192.168.1.8'
    server_port = 80
    tcp = TCPService(server_addr, server_port)
    tcp.start_service()

if __name__ == '__main__':
    main()
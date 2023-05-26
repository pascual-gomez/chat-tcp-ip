import socket
import pyaudio
import threading
import keyboard

# Audio
recording = False
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"
server_addr = '192.168.1.8'
server_port = 80

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def on_key_press(event):
    if event.name == 'r':
        recording = True
        print("Recording")
    elif event.name == 's':
        recording = False
        print("Stopped recording")

print("Starting client...")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_addr, server_port))
print(f"Connected to {server_addr}")
client_socket.settimeout(0.1)

while True:
    if recording == True:
        print("recording")
        try: 
            audio = stream.read(CHUNK)
            client_socket.send(audio)
        except OSError:
            pass
        except socket.timeout:
            pass
    elif recording == False:
        print("listening")
        try:
            audio = client_socket.recv(4096)
            if not audio:
                break
            print(f"Receiving audio from:  {server_addr}")
        except socket.timeout:
            pass

    if keyboard.is_pressed('r'):
        print("r pressed")
        recording = True
    elif keyboard.is_pressed('s'):
        print("s pressed")
        recording = False


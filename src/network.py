from pathlib import Path
from plyer import notification
import socket
import argparse
import struct
import threading
import json
import rsa

ADDR = "0.0.0.0"
PORT = 65535
FIXED_MSG_SZ = 4

PEER_PUBLIC = None

def recv_fixed(conn, size):
	buf = b""
	while len(buf) < size:
		chunk = conn.recv(size-len(buf))
		if not chunk:
			raise ConnectionError("Connection closed before all data was received")
		buf += chunk
	return buf

def receive_thread(conn, stop_event):
	global PEER_PUBLIC
	try:
		data = recv_fixed(conn, FIXED_MSG_SZ)
		(size,) = struct.unpack("!I", data)
		PEER_PUBLIC = json.loads(recv_fixed(conn, size).decode("utf-8"))

		while not stop_event.is_set():
			data = recv_fixed(conn, FIXED_MSG_SZ)
			(size,) = struct.unpack("!I", data)
			message = recv_fixed(conn, size).decode("utf-8")
			plaintext = rsa.decrypt(message)
			print(f"\nPeer: {plaintext}\nYou: ", end="")
			notification.notify(title="lanchatty", message=plaintext, timeout=5)
	except Exception as e:
		print(e)
	finally:
		print("Connection closed")
		stop_event.set()

def chat(conn):
	global PEER_PUBLIC

	stop_event = threading.Event()
	t = threading.Thread(target=receive_thread, args=(conn, stop_event), daemon=True)
	t.start()

	try:
		with open(Path("~/.lanchatty/rsa/public.key").expanduser(), "r") as f:
			public = f.read().encode("utf-8")
			conn.sendall(struct.pack("!I", len(public)))
			conn.sendall(public)
		
		while not PEER_PUBLIC:
			pass

		while not stop_event.is_set():
			message = input("You: ")
			message = rsa.encrypt(message, PEER_PUBLIC)
			if stop_event.is_set():
				break
			data = message.encode("utf-8")
			conn.sendall(struct.pack("!I", len(data)))
			conn.sendall(data)
	except Exception as e:
		print(e)
	finally:
		stop_event.set()
		try:
			conn.shutdown(socket.SHUT_RDWR)
		except Exception as e:
			print(e)
		conn.close()

def serve(s):
	s.bind((ADDR, PORT))
	s.listen()
	print("Waiting for connection...")

	conn, addr = s.accept()
	print(f"Connected with {addr}")
	chat(conn)

def join(s, host, port):
	s.connect((host, port))
	chat(s)


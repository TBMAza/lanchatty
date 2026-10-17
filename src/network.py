import os
import json
import struct
from pathlib import Path

import myrsa

from myglobals import ADDR, PORT, RSA_PATH, FIXED_MSG_SZ, PEER_PUBLIC_KEY

def recv_fixed(conn, size):
	buf = b""
	while len(buf) < size:
		chunk = conn.recv(size-len(buf))
		if not chunk:
			raise ConnectionError("Connection closed before all data was received")
		buf += chunk
	return buf

def send(conn, message: str, peer_public_key: dict = None):
	cipher = myrsa.encrypt(message, peer_public_key).encode("utf-8") if peer_public_key else message.encode("utf-8")
	conn.sendall(struct.pack("!I", len(cipher)))
	conn.sendall(cipher)

def recv(conn, encrypted: bool = True) -> str:
	data = recv_fixed(conn, FIXED_MSG_SZ)
	(size,) = struct.unpack("!I", data)
	cipher = recv_fixed(conn, size).decode("utf-8")
	message = myrsa.decrypt(cipher) if encrypted else cipher
	
	return message

def serve(s):
	global PEER_PUBLIC_KEY

	s.bind((ADDR, PORT))
	s.listen()
	print("waiting for connection...")

	conn, peer_addr = s.accept()
	with open(Path(f"{RSA_PATH}/public.key").expanduser(), "r") as f:
		my_public_key = f.read()
	send(conn, message=my_public_key)
	PEER_PUBLIC_KEY = json.loads(recv(conn, encrypted=False))
	
	print(f"connected with {peer_addr[0]}")

	return conn

def join(s, host: str, port: int):
	global PEER_PUBLIC_KEY

	print("connecting...")
	s.connect((host, port))
	PEER_PUBLIC_KEY = json.loads(recv(s, encrypted=False))
	with open(Path(f"{RSA_PATH}/public.key").expanduser(), "r") as f:
		my_public_key = f.read()
	send(s, my_public_key)

	print(f"connected with {host}")

	return s

def recv_thread(stop, conn, messages_q):
	try:
		while not stop.is_set():
			payload = ("message", recv(conn))
			messages_q.put(payload)
	except ConnectionError:
		if not stop.is_set():
			payload = ("disconnected", "connection closed by peer")
			messages_q.put(payload)
	except Exception:
		pass
	finally:
		stop.set()

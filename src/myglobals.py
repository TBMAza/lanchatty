import os
import queue
import threading

ADDR = os.getenv("ADDR", "0.0.0.0")
PORT = int(os.getenv("PORT", "6969"))
RSA_PATH = "~/.lanchatty/rsa"
FIXED_MSG_SZ = 4
PEER_PUBLIC_KEY = None

messages_q = queue.Queue()
stop = threading.Event()

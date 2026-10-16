import socket
import argparse
import threading

from chat_ui import ChatUI

import network
from myglobals import PORT, messages_q, stop


if __name__ == "__main__":
	# args
	parser = argparse.ArgumentParser()
	parser.add_argument("--serve", action="store_true")
	parser.add_argument("--join", action="store_true")
	parser.add_argument("--ip")
	args = parser.parse_args()

	# connect
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	conn = None
	if args.serve:
		conn = network.serve(s)
	elif args.join:
		if args.ip:
			conn = network.join(s, args.ip, PORT)
		else:
			print("usage: python main.py --join --ip <IPv4 address>")
	else:
		print("usage: python main.py --serve")
		print("       python main.py --join --ip <IPv4 address>")

	if conn:
		# receive thread
		rt = threading.Thread(target=network.recv_thread, args=(stop, conn, messages_q), daemon=True)
		rt.start()

		# chat UI
		chat_ui = ChatUI(conn)
		chat_ui.run()
		
		stop.set()
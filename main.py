import rsa
import network
import socket
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--serve", action="store_true")
	parser.add_argument("--join", action="store_true")
	parser.add_argument("--ip")
	args = parser.parse_args()

	rsa.keygen()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	if args.serve:
		network.serve(s)
	if args.join:
		if not args.ip:
			print("No ip address provided. Aborting.")
		else:
			network.join(s, args.ip, network.PORT)


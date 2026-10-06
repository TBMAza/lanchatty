import socket
import argparse
import struct


ADDR = "0.0.0.0"
PORT = 65535
FIXED_MSG_SZ = 4

def recv_fixed(conn, size):
    buf = b""
    while len(buf) < size:
        chunk = conn.recv(size-len(buf))
        if not chunk:
            raise ConnectionError("Connection closed before all data was received")
        buf += chunk
    return buf

def serve(s):
    s.bind((ADDR, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        try:
            while 1:
                data = recv_fixed(conn, FIXED_MSG_SZ)
                (size,) = struct.unpack("!I", data)
                data = recv_fixed(conn, size)
                print(data.decode("utf-8"))
        except ConnectionError:
            print("Disconnected")

def join(s, host, port):
    s.connect((host, port))
    while 1:
        message = input("You: ")
        data = message.encode("utf-8")
        s.sendall(struct.pack("!I", len(data)))
        s.sendall(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--join", action="store_true")
    parser.add_argument("--ip")
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if args.serve:
        serve(s)
    if args.join:
        join(s, "127.0.0.1", PORT)


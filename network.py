import socket
import argparse
import struct
import threading

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

def receive_thread(conn, stop_event):
    try:
        while not stop_event.is_set():
            data = recv_fixed(conn, FIXED_MSG_SZ)
            (size,) = struct.unpack("!I", data)
            data = recv_fixed(conn, size)
            print(f"\nPeer: {data.decode("utf-8")}\nYou: ", end="")
    except Exception:
        pass
    finally:
        print("Connection closed")
        stop_event.set()

def chat(conn):
    stop_event = threading.Event()
    t = threading.Thread(target=receive_thread, args=(conn, stop_event), daemon=True)
    t.start()

    try:
        while not stop_event.is_set():
            message = input("You: ")
            if stop_event.is_set():
                break
            data = message.encode("utf-8")
            conn.sendall(struct.pack("!I", len(data)))
            conn.sendall(data)
    except Exception:
        pass
    finally:
        stop_event.set()
        try:
            conn.shutdown(socket.SHUT_RDRW)
        except Exception:
            pass
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
        if not args.ip:
            print("No ip address provided. Aborting.")
        else:
            join(s, args.ip, PORT)


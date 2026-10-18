# lanchatty

Because sometimes you just need a quick local chat app and you do not want to install twenty different services, create an account, or get dragged into a 400 MB Electron app with a mascot made of anxiety.

lanchatty is a tiny LAN chat tool for two people on the same network (or the same VPN, if you are feeling fancy). It opens a socket, swaps public keys, and encrypts messages with RSA before sending them across the wire. Very small. Very local. Very much not a startup.

## What this thing does

- Creates a peer-to-peer chat connection over a local network
- Generates RSA keypairs and exchanges public keys
- Encrypts outbound chat messages before transmission
- Shows a simple Textual chat UI
- Sends desktop notifications and little sound effects when messages arrive
- Keeps the experience intentionally lightweight and small-bore

This is not a full-blown messaging platform. There are no rooms, no persistence, no friends list, no weird emoji reactions, and no nonsense. Just chat. The way it should be. Maybe.

## How it works

The app is intentionally simple:

1. One user runs the server side with `--serve`
2. The other connects using `--join --ip <host_ip>`
3. Both sides exchange public keys
4. Messages are encrypted using the peer's public key
5. A loop reads incoming socket data and pushes it into the UI queue

The actual network handling lives in `src/network.py`, the Textual UI is in `src/chat_ui.py`, and the RSA bits are in `src/myrsa.py`. Very clean. Very basic. Very "this was built by someone who wanted a chat app in a single afternoon".

## Requirements

- Python 3.10+
- A working local network or VPN
- Two machines that can reach each other over TCP

The repo already includes a `requirements.txt`, so you are not expected to go on a scavenger hunt for random packages.

## Installation

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you are on Windows, use the usual `venv` activation trick instead of pretending PowerShell is a personality.

## Usage

> Both users must be on the same LAN or connected to the same VPN.

### Host / server side

From the repo root:

```bash
cd src
python main.py --serve
```

This starts listening on the default local address and port and waits for a connection.

### Client / join side

On the other machine:

```bash
cd src
python main.py --join --ip <user_1_local_ip>
```

Example:

```bash
python main.py --join --ip 192.168.1.42
```

Once connected, the chat UI opens and you can type away like a responsible adult.

## Controls

The UI includes a couple of handy shortcuts:

- `Ctrl+S` — send current message
- `Ctrl+N` — toggle notifications
- The big text area at the bottom — where your masterpiece of conversation goes

## Configuration

The app uses a few defaults from `src/myglobals.py`:

- `ADDR = 0.0.0.0`
- `PORT = 6969`
- keys live under `~/.lanchatty/rsa`

You can override the port by setting the environment variable `PORT` before launching, if you are trying to be extra weird about it.

## Project structure

```text
lanchatty/
├── LICENSE
├── README
├── requirements.txt
└── src/
    ├── assets/
    │   ├── css/
    │   └── sounds/
    ├── chat_ui.py
    ├── main.py
    ├── myglobals.py
    ├── myrsa.py
    └── network.py
```

A quick map of the chaos:

- `src/main.py` — CLI entrypoint and thread setup
- `src/network.py` — socket connect, send/receive, key exchange
- `src/chat_ui.py` — Textual interface, notifications, queue handling
- `src/myrsa.py` — RSA key generation and encryption/decryption logic
- `src/myglobals.py` — shared constants and queue state

## Security notes

This is a local chat app with basic RSA encryption, which is cute and useful for a quick private local exchange. It is not a hardened messaging system and it is definitely not doing a bunch of auditing or fancy protocol stuff.

A few practical notes:

- It relies on a simple TCP connection and local network trust
- Keys are stored in `~/.lanchatty/rsa`
- It does not implement group chats, message history, or robust transport security
- It is small enough to understand without needing a PhD in cryptographic panic

So: good for LAN chats, not for "massive global secure communications platform" energy.

## Troubleshooting

### "It says waiting for connection... and then nothing happens"

- Make sure the host actually started with `--serve`
- Check that both devices are on the same LAN or VPN
- Confirm the target IP is correct
- If a firewall is being dramatic, open the port or disable the drama

### "Connection refused"

- Double-check the IP address
- Ensure the host is still running
- Make sure the port is reachable on the target machine

### "No message sounds or notifications"

- This is a feature, not a bug. Or maybe a bug. Either way, the app tries to show notifications when enabled and plays a sound after receiving a message.

## License

This project is licensed under the MIT License. That means you can use it, modify it, and distribute it, as long as the license notice stays intact. Very standard. Very boring. Very legally correct.

## Final thoughts

lanchatty is basically the "I need to chat with one person on my LAN without making my life worse" app. It's lightweight, a little goofy, and a bit rough around the edges, but it gets the job done without turning your machine into a digital circus.

If you want something more polished, there are already enough bloated apps in the world. This one is just here to help you send a message and move on. Which, honestly, is a pretty solid life philosophy.

from sympy import randprime
from egcd import egcd
import pickle
from pathlib import Path

RANDLO = 99999999
RANDHI = 999999999

def gcd(x, y):
    ret, _, _ = egcd(x, y)
    return ret

def keygen():
    if not Path("~/.ct2/private.key").expanduser().exists() and not Path("~/.ct2/public.key").expanduser().exists():
        p = randprime(RANDLO, RANDHI)
        q = randprime(RANDLO, RANDHI)
        while q == p:
            q = randprime(RANDLO, RANDHI)
        
        n = p*q
        phi_n = (p-1)*(q-1)
        
        e = randprime(2, phi_n)
        while gcd(e, phi_n) != 1:
            e = randprime(2, phi_n)
        _, d, _ = egcd(e, phi_n) # multiplicative inverse of e in modulus phi(n)
        d = d % phi_n

        private = (d, n)
        public = (e, n)

        Path("~/.ct2").expanduser().mkdir(exist_ok=True)
        with open(Path("~/.ct2/private.key").expanduser(), "wb") as f:
            pickle.dump(private, f)
        with open(Path("~/.ct2/public.key").expanduser(), "wb") as f:
            pickle.dump(public, f)

def encrypt(m, public):
    e, n = public
    width = (n.bit_length()+3)//4
    plain = [ord(i) for i in m]
    cipher = [pow(i, e, n) for i in plain]
    return "".join([f"{i:0{width}x}" for i in cipher])

def decrypt(c):
    with open(Path("~/.ct2/private.key").expanduser(), "rb") as f:
        private = pickle.load(f)
    d, n = private
    width = (n.bit_length()+3)//4
    cipher = [int(c[i:i+width], 16) for i in range(0, len(c), width)]
    plain = [pow(i, d, n) for i in cipher]
    return "".join([chr(i) for i in plain])

keygen()
with open(Path("~/.ct2/public.key").expanduser(), "rb") as f:
    public = pickle.load(f)
e = encrypt("lol", public)
print(e)
d = decrypt(e)
print(d)

import cryptography
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import x25519
#from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# https://chromium.googlesource.com/external/github.com/pyca/cryptography/+/1.2.3/docs/hazmat/primitives/key-derivation-functions.rst
# the other examples had no default default_backend imported
# in my script I have to define the backend
from cryptography.hazmat.backends import default_backend

# symmetric encryption
from cryptography.fernet import Fernet

# to get a string from any byte sequence
from base64 import standard_b64encode, standard_b64decode

# Client to client messages
from chat_utils import *
import json

def PublicKey_get_public_bytes(key):
    if cryptography.__version__ == '3.4.8':
        return key.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
    else:
        return key.public_bytes()


# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/x25519/
# X25519 key exchange

# also here explained
# https://crypto.stackexchange.com/questions/6307/why-is-diffie-hellman-considered-in-the-context-of-public-key-cryptography
# 

# just a single iteration/exchange (more would be safer)
# as we use hazmat.primitives.asymmetric.x25519 it's slightly different from original Diffie-Hellman
# https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange#General_overview
class DiffieHellman:
    def __init__(self):
        self.sharedSecret = None
        self.fernet = None
        self.private = x25519.X25519PrivateKey.generate()
        self.public = self.private.public_key()
        self.salt = b'CvpPQraOOImsfkaEUsdmmOeRivHbUPyvw8NZiXS1cxc='

    def derive(self, shared):
        return HKDF(    algorithm=hashes.SHA256(),
                        length=32,
                        salt=self.salt,
                        info=None,
                        backend=default_backend()
                        ).derive(shared)        

    def calculateShared(self, peer_public_key):
        shared = self.private.exchange(peer_public_key)
        byte_string = self.derive(shared)
        self.sharedSecret = standard_b64encode(byte_string)
        self.fernet = Fernet(self.sharedSecret)

    def createSharedSecret(self, sock, me):
        MESSAGE_ACTION_PREFIX = 'dh:'

        public_key_bytes = PublicKey_get_public_bytes(self.public)
        public_key_base64 = standard_b64encode(public_key_bytes)
        message = MESSAGE_ACTION_PREFIX + public_key_base64.decode() # (byte string) b'xxx'.decode() == string

        # The only Client to client communication is {"action": "exchange" ...}
        mysend(sock, json.dumps({"action": "exchange", "from": "[" + me + "]", "message": message}))
        response = json.loads(myrecv(sock))
        
        if 'action' in response and 'message' in response and \
                        response['action'] == 'exchange' and \
                        response['message'].startswith(MESSAGE_ACTION_PREFIX):

            peer_public_base64_string = response['message'][len(MESSAGE_ACTION_PREFIX):]
            peer_public_key_bytes = standard_b64decode(peer_public_base64_string)
            peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_key_bytes)
            self.calculateShared(peer_public_key)
            return True
        
        return False

    def encrypt(self, message):
        #fernet.encrypt(b'...')
        return self.fernet.encrypt(message.encode()).decode() if self.fernet != None else ""

    def decrypt(self, message):
        return self.fernet.decrypt(message.encode()).decode() if self.fernet != None else ""


if __name__ == "__main__":
    Alice = DiffieHellman()
    Bob = DiffieHellman()

    print(cryptography.__version__) 
    Alice.calculateShared(Bob.public)
    Bob.calculateShared(Alice.public)
    print(f'Alice public key: {PublicKey_get_public_bytes(Alice.public)}')
    print(f'Bob   public key: {PublicKey_get_public_bytes(Bob.public)}')
    print(f'Alice.shared == Bob.shared: {Alice.sharedSecret == Bob.sharedSecret}')

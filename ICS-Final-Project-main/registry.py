import hashlib # SHA-512
import secrets # Generate secure random numbers
import pickle
import threading

class Registry:
    def __init__(self, pickleFileName):
        self.pickleFileName = pickleFileName
        self.lock = threading.Lock()
        self.registry = {}

        # chat index does not exist, then create one
        try:
            with open(pickleFileName, 'rb') as file:
                self.registry = pickle.load(file)
        except IOError:
            pass
    
    def getSignature(self, password, salt):
        #   r : blocksize
        #   n : CPU cost parameter >1
        #   p : parallelization parameter >0
        return hashlib.scrypt(password.encode(), salt=salt, n=256, r=8, p=1, dklen=256)

    def add(self, user, password):
        if user in self.registry:
            return (False, "User already exists")
        else:
            salt = secrets.token_bytes(64)
            signature = self.getSignature(password, salt)
            self.registry[user] = (signature, salt)
  
            # we update the pickle file for each registered user
            # If another users registers while we still write 
            # the pickle file from the register of the last user
            # pickle.dump() and close(file) need to complete first!!!
            with self.lock:
                with open(self.pickleFileName, 'wb') as file:
                    pickle.dump(self.registry, file)
  
            return (True, "")

    def login(self, user, password):
        if user in self.registry:
            secret = self.registry[user]
            signature = self.getSignature(password, secret[1])
            if secrets.compare_digest(signature, secret[0]) == True:
                return (True, "")

        return (False, "User and password don't match")

def testAdd(registry, user, password):
    print(f"add {user} {password}:", registry.add(user, password))

def testLogin(registry, user, password):
    print(f"login {user} {password}:", registry.login(user, password))

if __name__ == "__main__":
    r = Registry()
    testAdd(r, "Leo", "aa")
    testAdd(r, "Otto", "bb")
    testAdd(r, "Otto", "bb")
    testLogin(r, "Leo", "ab")
    testLogin(r, "Leo", "aa")
    testLogin(r, "Otto", "aa")
    testLogin(r, "Otto", "bb")
    testLogin(r, "Heiner", "bb")

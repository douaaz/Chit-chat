import string  # string.punctuation

# TODO: make isPasswordCompliant() return error messages like isUserNameCompliant()
def isPasswordCompliant(password):
    if len(password) >= 8 and not any(ch.isspace() for ch in password):
        if any(ch.isupper() for ch in password) and \
            any(ch.islower() for ch in password) and \
            any(ch.isdigit() for ch in password) and \
            any(ch in string.punctuation for ch in password):
            return True
    return False

def isUserNameCompliant(username):
    if len(username) >= 5:
        if username.isprintable():
            if any(ch.isalpha() for ch in username):
                return (True, "")
            else:
                return (False, 'Please include letters')
        else:
            return (False, 'Use only letters, numbers, punctuation and space')
    else:
        return (False, 'User name must be at least 5 letter long')

def testPassword(password):
    print(f"password: {password} is", '' if isPasswordCompliant(password) else "not", 'compliant')

def testUsername(username):
    print(f"isUserNameCompliant({username}) returns {isUserNameCompliant(username)}")


if __name__ == "__main__":
    testPassword("11111111")
    testPassword("aaaaaaaa")
    testPassword("AAAAAAAA")
    testPassword("Aaaaaaaa")
    testPassword("A!aa aa1")
    testPassword("Aaaaaaa1")
    testPassword("A!abaa1")
    testPassword("A!aabaa1")
    testPassword("A!aabaa1aaaaaaaaaaaaaaaaaaaaa")

    testUsername('11111')
    testUsername('aaaa')
    testUsername('aaaaa') 
    testUsername(b'aaaaa\x01'.decode()) 


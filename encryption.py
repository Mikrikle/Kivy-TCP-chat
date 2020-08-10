SECRET_KEY = 10


def encryptDecrypt(mode, message):
    global SECRET_KEY
    key = SECRET_KEY
    final = ''
    for symbol in message:
        if mode == 'E':
            final += chr((ord(symbol) + key))
        else:
            final += chr((ord(symbol) - key))
    return final
import time
import hmac
import hashlib

def sign(key, secret, method, requestPath, body=""):
    timestamp = str(int(time.time()))
    combined = str(timestamp) + method + requestPath + body
    
    signature = hmac.new(bytes(secret, "utf-8"), msg = bytes(combined, "utf-8"), digestmod = hashlib.sha256).hexdigest().upper()

    return signature


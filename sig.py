import hmac
import hashlib

def sign(secret, timestamp, method, requestPath, body=""):
    combined = timestamp + method + requestPath + body
    
    signature = hmac.new(secret.encode('utf-8'), combined.encode('utf-8'), digestmod=hashlib.sha256).digest()

    return signature


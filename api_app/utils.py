import os
import base64


def generate_referral_token(len=8):
    token = os.urandom(len)
    return base64.b64encode(token).decode()

import os
import binascii
import uuid


def get_token():
    return binascii.hexlify(os.urandom(20)).decode()


def generate_userid():
    return uuid.uuid4().hex[:15]

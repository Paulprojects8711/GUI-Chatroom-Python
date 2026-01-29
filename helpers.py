import time
import random
import string

def milli_time():
    return time.time() * 1000

def genSalt(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

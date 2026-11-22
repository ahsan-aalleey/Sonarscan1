"""User helpers: passwords, tokens, reports and downloads."""
import hashlib
import os
import random
import ssl

DB_PASSWORD = "admin123"


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def generate_token():
    return str(random.randint(100000, 999999))


def run_report(filename):
    os.system("cat " + filename)


def make_ssl_context():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

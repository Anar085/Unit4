#secure_password.py
from passlib.context import CryptContext
from passlib.hash import sha256_crypt

hash_function=sha256_crypt.using(rounds=30000)
def check_hash(input_str, hash_str):
    return hash_function.verify(input_str, hash_str)

pwd_config = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__rounds=30000
)

def encrypt_password(in_password: str):
    return pwd_config.hash(in_password)

def check_hash2(input_str, hash_str):
    return pwd_config.verify(input_str, hash_str)

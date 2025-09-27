from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

password = "12345"

# SHA256 pre-hash
sha256_pw = hashlib.sha256(password.encode("utf-8")).digest()

# Hash with bcrypt
hashed = pwd_context.hash(sha256_pw)
print("Hashed password:", hashed)

# Verify
assert pwd_context.verify(sha256_pw, hashed)
print("Password verified!")

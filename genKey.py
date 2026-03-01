import os
import base64

# 1️⃣ Generate a secure random key (32 bytes = 256 bits)
key_bytes = os.urandom(32)

# 2️⃣ Encode the key as a base64 string
key_b64 = base64.b64encode(key_bytes).decode('utf-8')

print("Base64 encoded key:", key_b64)

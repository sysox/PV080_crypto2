# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Data Authentication and Integrity

# By purely encrypting data, we only ensure its **confidentiality**. However, there are other desirable security properties.

import secrets
from pv080_crypto import XOR, sha256_hash, chacha20_encrypt, chacha20_decrypt, create_mac, verify_mac
from pv080_crypto import send_message, recv_message


# ## 1. Hash Functions

# When data are transferred via a network, they may get corrupted, either by accident or by an attacker. We want to be able to confirm that this has not happened. In other words, we want to check the **integrity** and **authenticity** of the data.
#
# The most naive approach is to use **hash functions**.

# **Task 1.1**: Download the tar archive [openssl-3.1.0.tar.gz](https://www.openssl.org/source/openssl-3.1.0.tar.gz) from [OpenSSL
# Cryptography and SSL/TLS Toolkit](https://www.openssl.org/source/).

# +
def download(url: str) -> str:
    import requests
    filename = url[url.rfind("/")+1:]
    r = requests.get(url, allow_redirects=True)
    with open(filename, 'wb') as file: 
        file.write(r.content)
        print(f'Downloaded file={filename} from url={url}')
    return filename

url = 'https://www.openssl.org/source/openssl-3.1.0.tar.gz'
download(url)
# -

# Then load the file in binary mode and hash it using the function [`sha256_hash`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.sha256_hash).

with open('openssl-3.1.0.tar.gz', 'rb') as file:
    pass

# Verify that the computed hash matches the one (`aaa925ad9828745c4cad9d9efeb273deca820f2cdcf2c3ac7d7c1212b7c497b4`) published in the [file with SHA256 hash](https://www.openssl.org/source/openssl-3.1.0.tar.gz.sha256) provided by OpenSSL.



# ## 2. Data Authentication via Hash Functions

# In the rest of the seminar, you will work in groups of 3. Find 2 classmates and decide on your roles: the **client**, the **bank**, and the **attacker**.
#
# - The client wants to send the message `"Hi bank I want to send 000000010.00 USD to Bob"` to the bank.
# - The bank wants to verify that the message came from the client and was not corrupted.
# - The attacker (Eve) wants to modify the message to say `"Send 999 USD to Eve"`.
#
# The message is not confidential, so it **can** be sent in plaintext.

# Set UČOs for the communication. The attacker does *not* set her UČO, because she will pretend to be the client.

client_uco = 0
bank_uco = 0

# **Task 2.1**: Try using [`sha256_hash`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.sha256_hash) to ensure message integrity:
# 1. The client sends the message together with its hash.
# 2. The bank receives the message, computes its hash, and verifies that it matches the received hash.



# **Task 2.2**: Repeat the previous task, but let the attacker replace the message before it is received by the bank:
# - Can the attacker replace the message without the bank noticing?



# ## 3. Data Authentication via Encryption 

# Clearly, sending a hash together with the message is not enough to ensure the authenticity of the message. In fact, the client and the bank will need to use keys - either a shared symmetric key, or asymmetric key pairs.

# **Task 3.0**: We will use Vernam cipher ([`XOR`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.XOR)) with deterministic generation of the keystream. The attacker should not know it (or at least pretend to not know it) and **not use it**. The Vernam is used to simplify the encryption but everything will work same way for CTR. The client should use [`XOR`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.XOR) to encrypt the message and send it to the bank.

# The key should be as long as the message
msg = b'Arbitrary message'
symmetric_key = bytes([i for i in range(len(msg))])


# The client should use [`XOR`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.XOR) to encrypt the message and send it to the bank.

# +
# Client - encrypt
# -

# The bank should use [`XOR`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.XOR) to decrypt the message.

# +
# Bank - decrypt
# -

# **Task 3.1**: Repeat the previous task, but let the attacker intervent:
# - Can the attacker (Bob) meaningfully alter the message if he knows the message format? The message format is `"Send XXXXXXXXX.XX USD to YYY"`.
# - Can the attacker change the content of the message so bank will sent larger amount?
#
# Try to attack multiple times.

# +
# Client - encrypt

# +
# Attacker - replace the message (knows the format of the original message)

# +
# Bank - decrypt
# -

# **Task 3.2**: Bank added checksum as additional layer of integrity protection. But the checksum is just XOR of all bytes of the message and is appended to ciphertext. Attack the communicatioon so that bank will sucessfuly verify the message. Try two attacks: one where checksum and bytes of the ciphertext are changed, other where only ciphertext is chagned (not the checksum). 

# +
def compute_checksum(msg: bytes) -> bytes:
    res = 0
    for b in msg:
        res ^= b
    return bytes([res])

def verify_checksum(msg: bytes, checksum: bytes) -> bool:
    return checksum == compute_checksum(msg)
# -

# Client




# Attacker who does not know the format, he knows only that the last byte is the checksum 


# +
# Bank
# -

# ## 4. Data Authentication via MACs

# As we can see, we can ensure message authenticity neither by sending hashes, nor by symmetric encryption alone. The advantages of both are combined in the so-called **MACs** (Message Authentication Codes).

# **Task 4.0**: Decide on a symmetric key to use in the MAC and share it among the client and the bank. Again, the attacker should pretend not to know it.

# The key is 32 bytes
symmetric_key = bytes([i for i in range(1, 33)])

# **Task 4.1**: Use a MAC to ensure message authenticity:
# 1. The client sends the message together with its MAC (use [`create_mac`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.create_mac)).
# 2. The bank receives the message and MAC, then verifies the MAC (use [`verify_mac`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.verify_mac)). 

# **Task 4.2**: Repeat the previous task, but let the attacker intervent:
# - Can the attacker alter the message without the bank noticing?



# **Task 4.3 (Bonus)**: Implement the function `my_cbc_mac` using [`pad`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.pad) and [`aes_cbc_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_cbc_encrypt). A CBC-MAC is simply the last block of the AES-CBC-encrypted data with an IV consisting of zero bytes.

# +
from pv080_crypto import pad, aes_cbc_encrypt

def my_cbc_mac(key: bytes, data: bytes) -> bytes:
    pass
# -

# Verify that `my_cbc_mac` works identically to `create_mac`.

msg = b'Send 100 USD to Bob'
mac = create_mac(symmetric_key, msg)
my_mac = my_cbc_mac(symmetric_key, msg)
assert mac == my_mac


# **Task 4.4 (Bonus)**: An alternative to CBC-MAC is the so-called [HMAC](https://en.wikipedia.org/wiki/HMAC). Implement the function `my_hmac` by following its definition in [RFC 2104](https://www.rfc-editor.org/rfc/rfc2104.txt). You can use the functions [`XOR`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.XOR) and [`sha256_hash`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.sha256_hash).

def my_hmac(key: bytes, data: bytes) -> bytes:
    pass

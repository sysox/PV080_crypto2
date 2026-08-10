# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     custom_cell_magics: kql
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Asymmetric and Hybrid Encryption

# %% [markdown]
# We will continue using the `pv080_crypto` library today. Let's import the necessary functions.

# %%
from pv080_crypto import aes_encrypt, aes_decrypt
from pv080_crypto import rsa_encrypt, rsa_decrypt, publish_key, fetch_key
from pv080_crypto import send_message, recv_message
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from measurements import measure_aes_speed, measure_rsa_speed
import secrets

# %% [markdown]
# # <span style="color:red">RSA</span>

# %% [markdown]
# ## 1. Asymmetric Encryption (RSA)

# %% [markdown]
# In symmetric encryption, we used random bitstrings as keys. In asymmetric encryption, keys are usually numbers with specific properties. Functions from `pv080_crypto` make use of the [`rsa.RSAPrivateKey`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey) class from the `cryptography` library.

# %% [markdown]
# **Task 1.1**: See the introduction of the [asymmetric cryptography module](https://pv080.fi.muni.cz/docs/api/asymmetric.html) in the `pv080_crypto` documentation and find out how to generate an RSA key pair.

# %%
# Generate an RSA private key

# %%
# Obtain the public key from the private key
public_key = None #replace None

# %% [markdown]
# **Task 1.2**: Use [`rsa_encrypt`](https://pv080.fi.muni.cz/docs/api/asymmetric.html#pv080_crypto.asymmetric.rsa_encrypt) and [`rsa_decrypt`](https://pv080.fi.muni.cz/docs/api/asymmetric.html#pv080_crypto.asymmetric.rsa_decrypt) to encrypt and decrypt `msg` using the generated key pair.

# %%
msg = b'Lorem Ipsum'

# %% [markdown]
# Verify that the decrypted plaintext matches the original message.

# %%

# %% [markdown]
# **Task 1.3**: Can you use [`rsa_encrypt`](https://pv080.fi.muni.cz/docs/api/asymmetric.html#pv080_crypto.asymmetric.rsa_encrypt) to encrypt messages of *arbitrary* length? Try encrypting a very large message, e.g. of size 10000 bytes.

# %%
# Try encrypting this message
very_long_msg = b'\x00' * 10000

# %% [markdown]
# **Task 1.4**: What is the maximal length of message that we *can* encrypt using RSA? RSA uses OAEP padding working with SHA256 (hash length = 32 bytes = 256 bits) hash function hence **bytes** of padding **padding length = 2*length of hash + 2**.
#
# Guess the maximal size of message (in bytes) and verify the guess using [`rsa_encrypt`](https://pv080.fi.muni.cz/docs/api/asymmetric.html#pv080_crypto.asymmetric.rsa_encrypt).

# %%
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

maximal_length = 200
print(f"RSA{public_key.key_size}: can encrypt message up to {maximal_length} bytes")

# This should work
long_msg = b'\x00' * maximal_length
rsa_encrypt(public_key, long_msg)

# This should not work
longer_msg = b'\x00' * (maximal_length + 1)
try:
    rsa_encrypt(public_key, longer_msg)
except ValueError:
    print('Plaintext too long.')

# Hint:
# - For RSA-OAEP with SHA-256, the maximal plaintext length is:
#     max_len = k - 2*hLen - 2
#   where k is RSA modulus length in bytes (key_size // 8) and hLen is hash output length in bytes (32 for SHA-256).
# - Verify your guess experimentally: one message of length max_len should encrypt, length max_len+1 should fail.
#
# Try here:
# k = public_key.key_size // 8
# hLen = 32  # SHA-256 output length in bytes
# max_len = k - 2*hLen - 2
# msg_ok = b'\\x00' * max_len
# msg_too_long = b'\\x00' * (max_len + 1)

# %% [markdown]
# **Task 1.5 (Bonus)**:  Implement functions `my_rsa_encrypt` and `my_rsa_decrypt` without using any cryptography library. You may use Python built-in functions such as [`pow`](https://docs.python.org/3/library/functions.html#pow), [`int.to_bytes`](https://docs.python.org/3/library/stdtypes.html#int.to_bytes), and [`int.from_bytes`](https://docs.python.org/3/library/stdtypes.html#int.from_bytes). 
#
# - Use the three-argument form `pow(m, e, n)` for modular exponentiation (do not use `m**e % n`, as `pow(m, e, n)` is more efficient and avoids very large intermediate values).
#
# - Since RSA operates on integers but messages are typically byte sequences (text), use `int.from_bytes()` to convert bytes to an integer before encryption and `int.to_bytes()` to convert the decrypted integer back to bytes.
#
# Implement “textbook” RSA only; no padding is required.

# %%
def my_rsa_encrypt(public_key: rsa.RSAPublicKey, plaintext: bytes) -> bytes:
    e = public_key.public_numbers().e
    n = public_key.public_numbers().n
    # Use `e` and `n` to encrypt `plaintext`
    pass

def my_rsa_decrypt(private_key: rsa.RSAPrivateKey, ciphertext: bytes) -> bytes:
    d = private_key.private_numbers().d
    n = private_key.public_key().public_numbers().n
    # Use `d` and `n` to decrypt `ciphertext`
    pass


# %% [markdown]
# Verify that your functions work. Encrypt a message using `my_rsa_encrypt` and then decrypt it using `my_rsa_decrypt`.

# %%

# %% [markdown]
# ## 2. Communication using RSA

# %% [markdown]
# Last week, you used [`send_message`](https://pv080.fi.muni.cz/docs/api/messaging.html#pv080_crypto.messaging.send_message) and [`recv_message`](https://pv080.fi.muni.cz/docs/api/messaging.html#pv080_crypto.messaging.recv_message) to exchange messages with your classmates. To exchange RSA-encrypted messages, you also need to be able to publish your public key.

# %% [markdown]
# **Task 2.1**: Use [`publish_key`](https://pv080.fi.muni.cz/docs/api/asymmetric.html#pv080_crypto.asymmetric.publish_key) to make your public key visible to your classmates. Then retrieve it using [`fetch_key`](https://pv080.fi.muni.cz/docs/api/asymmetric.html#pv080_crypto.asymmetric.fetch_key).

# %%
# %% [markdown]
# Verify that the fetched key is yours by encrypting something with it and decrypting with your private key.

# %%
# %% [markdown]
# **Task 2.2**: Fetch a public key of your classmate and exchange encrypted messages with them. Two follwoing cell are for sender and receiver.

# %%
# Fetch the public key

# Encrypt a message using RSA

# Send the encrypted message

# %%
# Receive a message from the classmate

# Decrypt the received message

# %% [markdown]
# **Task 2.3 (Bonus)**: Use the functions `my_rsa_encrypt` and `my_rsa_decrypt` from Task 1.4 to exchange messages over the network. Can messages encrypted using `my_rsa_encrypt` be decrypted using `rsa_decrypt` and vice versa? Why?

# %%

# %% [markdown]
# # <span style="color:red">Hybrid Encryption</span>

# %% [markdown]
# ## 3. Hybrid Encryption: Motivation

# %% [markdown]
# The speed of AES and RSA algorithms differs greatly. While RSA can be used to share a key publicly, it is not that practical for large messages. We can compare encryption speed by encrypting messages of different sizes. AES encrypts much larger messages in *roughly* the same time.

# %% [markdown]
# **Task 3.1**: Play with message lengths. How much faster AES is compared to RSA?

# %%
aes_key = secrets.token_bytes(16)
rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Play with the length of the message
message_aes = b"\x00" * 10000000
message_rsa = b"\x00" * 20000
# Note: RSA cannot encrypt such a long message in one call; measure_rsa_speed() measures repeated RSA operations internally.
print(f"AES message is {len(message_aes)/len(message_rsa) } times larger than RSA.\n")

measure_aes_speed(aes_key, message_aes)
measure_rsa_speed(rsa_key, message_rsa)
# %% [markdown]
# ## 4. Communication using Hybrid Encryption

# %% [markdown]
# **Task 4.1**: Replicate the worked-out paper diagram in front of you. Decide who represents which party (we have **tthe bank** and **the client**).
#
# Then carry out the following communication between tthe bank and the client:
# 1. Tthe bank publishes its RSA public key.
# 2. The client uses RSA encryption to share a symmetric (AES) key with tthe bank.
# 3. The parties use AES to exchange the following two messages:
#
# *Bank*: `"What amount do you want to transfer?"`</br>
# *Client*: `"Amount: 000000100.00 USD"`

# %% [markdown]
# Set your UČOs for the communication here:

# %%
bank_uco = 123456
client_uco = 987654


# %% [markdown]
# ### Bank's point of view

# %% [markdown]
# Generate an RSA key pair and publish your public key.

# %%

# %% [markdown]
# Receive the encrypted key AES key from the client, decrypt it, and send the first message.

# %%

# %% [markdown]
# Receive the AES-encrypted reply from the client, decrypt it, and print it.

# %%

# %% [markdown]
# ### Client's point of view

# %% [markdown]
# Fetch tthe bank's public key. Then generate an AES key, encrypt it using RSA, and send it to tthe bank.

# %%

# %% [markdown]
# Receive the first AES-encrypted message from tthe bank, decrypt it, and print it. Then encrypt a reply and send it to tthe bank.

# %%

# %% [markdown]
# **Task 4.2 (Bonus)**: In the previous task, at least 3 messages had to be transmitted via the network.
#
# Now assume that the bank does not need to send the question (`"What amount do you want to transfer?"`). Can you reduce the number of transmitted messages to one? Discuss with your classmate and try to implement the solution.

# %%
# %% [markdown]
# ## Extra bonus - Attacking Text-book RSA

# %% [markdown]
# **Task 5 (Bonus)**: In this task, your goal is to take advantage of weaknesses of **text-book RSA**.
#
# In the scenario, you are supposed to decrypt the ciphertext `ct`. While the corresponding private key is provided, this is supposed to be a challenge, so you are supposed to decrypt this ciphertext without actually decrypting it - **you are allowed to use the key to decrypt any ciphertext other than the provided ciphertext**. Can you still find the original plaintext while respecting this limitation?

# %% [markdown]
# You are provided with an implementation of text-book RSA that was used to obtain the ciphertext.

# %%
def my_rsa_encrypt(public_key: rsa.RSAPublicKey, plaintext: bytes) -> bytes:
    e = public_key.public_numbers().e
    n = public_key.public_numbers().n
    # Convert the plaintext bytes to an integer, treat them as big-endian
    plaintext_num = int.from_bytes(plaintext, byteorder='big')
    # c = m ^ e (mod n)
    ct = pow(plaintext_num, e, n)
    # Convert the ciphertext back to bytes, the size should correspond to key size
    return ct.to_bytes(public_key.key_size // 8, byteorder='big')

def my_rsa_decrypt(private_key: rsa.RSAPrivateKey, ciphertext: bytes) -> bytes:
    d = private_key.private_numbers().d
    n = private_key.public_key().public_numbers().n
    # Convert the plaintext bytes to an integer, treat them as big-endian
    ciphertext_num = int.from_bytes(ciphertext, byteorder='big')
    # m = c ^ d (mod n)
    pt = pow(ciphertext_num, d, n)
    # Convert the plaintext back to bytes, the size should correspond to key size
    # Strip the leading zero bytes to obtain the original message
    return pt.to_bytes(private_key.key_size // 8, byteorder='big').lstrip(b'\x00')


# %% [markdown]
# Load the private key and public key:

# %%
private_key_string = '308204be020100300d06092a864886f70d0101010500048204a8308204a40201000282010100fb2f1b84d36864d2e689b178114d408099a98bf7b8d446f78e8ebe6d74d0f2f9cc2972ab6649ea4c6426073b83a7aff7ad6d50a58b5c09bb865d780b29ec9fcbf335411ff3ec15a8da941acc5478a91bb9eec13931b36166aa7ad16e1b3f2f4aad1d31b082d1cac67db929e178d20c3dfad3df8b39e1cb502aa6dd11a2ea47340755635138da9f640fc5f453574c47b4d8cbb80b78cb14265f39143a8b9f11c2934b7e0daa2046b59eb290db2710733bf7e554250710dff21c59b0a01dcd67414c65ac5073197544d986b830a19f87cf44d77775baaa578abd98535330ca131a0b080cb5e5c56d9aa03957df3c8c76cb73e50e0ad88c7e5e6890cb82e650944502030100010282010001cbadea2eaab5e1ce1518e82f537a8d10cc25fc80dd3f9ea06dc3cdbb828ce21d44049656165c2eec9e5af9e1708ef0f9d3e8ba2e3b5bb473faf2133e5afb2f758f21668d9357fa4b89b881526f446236db8e950e9666315a31a392a26e3ab3d175fe77710ff7dfa06174fbb025ec417b2c0d928cb8e0ffb3365b29379d6e21dcf55f31b765973bb6900c5b1e8b43db8431fc09dae1dbaef5a7413f3efbd91be97dc86866922f9a034dad12334502e35d1e611d19bdf626388360425f08ee105963a6cfde88effd6abce2f5eefcabda25d759e6f48dffc9ba61c918223e3fdc02410a17709e4a4dc60ae98cf1d96d7330db4c15df9dfd9e1d5bb3e1fc04167102818100fffd3134b0c5f76e6f780a84c057f2f9a06524f55f247b08da784891e842b592746ce42d3e4f4e94473176c8d4eedb8fedd10093978d1c20e4434b1a7f0827ab4f89722a129976d522b78e896e81886c4cfe6abbab31e175bbd30f51564bd1d68acbc25eaec1be3bc043879ed8d73ac4c21b8416c1236ff961ba1eed4921ed9d02818100fb31dcd22b0548fd1d4af3d30407827a2abd540fdc0fbfbce3fcaef8902f3ab6c26ad06b397f7527219405a5f14c668fe51019ee681aa3349461618fd76f21ed2b0860a9544f9f2a3196c5c174e7716a3d3e8d3e0baba34fa79a6260bf3c5acdf524e0e459dc1c9ee3f4f1636a55b845e9877400d25ca2251bb3d8323853d4c9028180071be4ededaad1c04360360a91bcdf868729c7e8f8876ed3441deb06024937f9a53a10ec20badb17cb1258962333aeed4451758ea3bacb792e5da00c5052cda738423ce56636d4d1fe70d28886851a60c792992c3508e195ff6d5113952dedd9e368dd30fbf16d730357dcc0508d4998853b76639b617c8e946432cfac24411102818100f038a526d04183a59be7dbf946f72f8e49653a08d8b8aef2a34d38bf389412204919012c29967ca0e979b75514c7ada59ab7a534db95edd210bc7822a931fc4de54363bd4b85c17f06615bc940553d9f0de6ce0831fcf876ea9fb7c931d934359664a83578c20914e2879279326dbb8610689b4555e784a0dc37475fef822c11028181009965c1b311579db3c9812d2491257059dd2c415f705d7c18d550681863f376e3249fcfec14d17f2e9fb249373935af9f2eed2173f5d41aa041a0b085e5425a91f5362d00be6023920c7d9433b896f16deced61ecce96c1a86bc0b9e0a2d97e81ab4290e2a7894f22d2c05d7c489eccf2307ca0373bbceeaecfbcbe04abb081f4'
private_key = serialization.load_der_private_key(bytes.fromhex(private_key_string), password=None)
public_key = private_key.public_key()

# %% [markdown]
# Your goal is to decrypt the following ciphertext (while respecting the limitation):

# %%
ct = b"w\xdd'\xc9\xe0\xad\xddJ\xe5\xaf\x0f^\x14t\xfd\xdc+J\x03Dm\x9c\x8a\xd9js\xa4=\x8e\xcc#I\xe7hb\xa5f\xd9&\x81\xd2/v\x03\xab\xf3\xed>tk\xbaD\xa7W\x00\x00\xaa6\x0f%\x85Ye\x82\x80\x9e\xfb\xca\xcc \xd8j\xc89\xf4j\xb4\xdf\xf9Q)\x9c*,X\x8c\x8c\x84pt\t\x1e)\x9a:s\x02\xd0\x9e\x0c\xdc=m\xf5-\x18\xf1\xb1\x9fU\x0c\xf0\xec\xff>\xec\xc2\x0b\x8c\xc3\xa8\xf9\x99\xf9?FBo\xc5\xac\xfcNN\x97M\x02\xbf\xea#\n\xae\x9e\xf5f\xf1vf\xe4\x1e\x15\x02\xc8\x99\xf9\x9c\xe8\x9e\xd9\x99\xafU\x0b\xb8\x9d\xe3\xbd\xf7r\xcf\x8c\x12\x1b\x01~ \x8fe\x80\x9d\x15\x0c9l\x86\xf8\xcfy\\\xc5\xc4\x85\xcb\xa5\xc2\xcb\xe6Q\x00t\x04!Ajs\xfd\x1a\xad?l\xb5~\x93\x13Xh\t\xc37@{\xeb@t&.g\x94\x93j7,1\x00\x0f\xbek\xf0\xe0\x19X\x05O4\x90\xa8\x16\xdc\xe2s\xd4\xe0z\xb1\xa6uW"

# %% [markdown]
# If you have no idea what to do, you can obtain a hint by decrypting following ciphertext (which you are allowed to decrypt directly):

# %%
hint = b'\x9a>\xee\xfcA\xfa5\x07K\xdb\xe4\xab\xe3\x8f"O\x89%\x17\xa0\x1c\x88Fx\xd2\xd2\x95\x17sJ\xc3\xbd)\x07\xe6/\x93\xdeg5\xfc,\x14\x84\xea\xa8-\xbb\x9a\x05\xc0\xf6\x1f\x010ks\x17@h\x9av\xe8\x99i\x8b\xe4q\xc02\xe28$\xad\xa3\xc6}sB\xd5u\x9dl\xd2\xa7\'\xad\xe5\xed\xa6\xdc\x90\x01\xc65S\x13\x17\x91\xe5\xaa`\xcd)\x113\xc1\xaa\x96\xd5\xd1\xc3\x1dIG\x84\xf3\xdfD\xb7g\xdaR\'\xd2\x85\xc3\x11\xae\xbf\x05\xa6G\xb9\x16\x01QBL\xca6\xaa\x9d\x0fb\x1e\xf1;\xa3\tj\xff\xaeK\xa6T#\x02\x18\xe5\x0cIv6o7J\xcfP\xeb\xe3\xf2\xccUmR\x15\xe8\x9e-\xd86c2\xce\x04Q\x7f;\x16}i\x16\x90\'R\x85\x17|\x01\xffMn\x84Y\x1dtH\xfe\xff]V\xe0"Cb\x7f}\x12\xaa\xd7\x0f\xb7\x0b\x04\xae\xc3~\x9d\x8duI`f\xd9\x89<j\xe9\xcb\x82\xc5~\xc0\xce\xfc\xf17\xaekyA\xc0\xadQ\xa1'

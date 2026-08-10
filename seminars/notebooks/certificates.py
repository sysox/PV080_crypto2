# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
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

# # Seminar 07: Signatures, Certificates, Challenge-Response

# Today, you will use many familiar functions from previous cryptography seminars but a lot of new ones too. Run the cell below to import them all.

from pv080_crypto import rsa_encrypt, rsa_decrypt
from pv080_crypto import create_signature, verify_signature, verify_cert_signature
from pv080_crypto import send_message, recv_message, publish_key, fetch_key
from pv080_crypto import request_cert, verify_challenge, fetch_cert
from pv080_crypto import load_cert, store_cert, extract_names, create_csr
from cryptography.hazmat.primitives.asymmetric import rsa

# ## 1. Digital Signatures

# In the last cryptography seminar, we used MAC functions to ensure **data authentication**. The same security property can be ensured with asymmetric methods, using digital signatures.

# **Task 1.1:** Exchange signed messages with your colleague by following the steps below.

# Set UČOs for the communication.

my_uco = 485305
partner_uco = 485305

# Generate an RSA key pair. See the [documentation](https://pv080.fi.muni.cz/docs/api/asymmetric.html) of `pv080_crypto` if you do not recall how. Do not forget to publish your public key using the function [`publish_key`](https://pv080.fi.muni.cz/docs/api/asymmetric.html#pv080_crypto.asymmetric.publish_key).



# Send a message **together with its signature** to your colleague. Use the function [`create_signature`](https://pv080.fi.muni.cz/docs/api/asymmetric.html#pv080_crypto.asymmetric.create_signature) to sign the message, and the same [messaging API](https://pv080.fi.muni.cz/docs/api/messaging.html) as in the previous seminars.



# Receive the message and its signature from your colleague and verify the signature using [`verify_signature`](https://pv080.fi.muni.cz/docs/api/asymmetric.html#pv080_crypto.asymmetric.verify_signature). Remember that you must download your colleague's public key using [`fetch_key`](https://pv080.fi.muni.cz/docs/api/asymmetric.html#pv080_crypto.asymmetric.fetch_key).



# **Task 1.2 (Bonus):** With the knowledge of hybrid encryption and digital signatures, we are getting close to modern cryptographic protocols, such as TLS. But there is still one problem that needs resolving.
#
# Assume that your seminar tutor believes that when he/she downloads a public key using `fetch_key(uco=123456)`, the downloaded public key **truly belongs** to a student with UČO `123456`. 
#
# Imagine that your colleague ate your sandwich without your consent. As a revenge, you want your colleague to fail the PV080 course. Can you convince your tutor that your colleague sent him/her a signned, plaintext, message saying `"I confess to cheating at homeworks."`?

tutor_uco = 232886

# ## 2. Obtaining a Public Key Certificate

# In this part, your ultimate task will be to obtain a certificate for your public key. The certificate will **bind your identity** (UČO) to the key.

# ### Certificate Authority

# In a real-world scenario, you would want your certificate issued by a well-known certificate authority, e.g. [Let's Encrypt](https://letsencrypt.org/). The certificates of such authorities usually come preinstalled with operating systems.
#
# For the purposes of this seminar, our own **PV080 Server** root CA will suffice. Its certificate, `pv080-root.crt`, is included in this repository.

# **Task 2.1:** Use the function [`load_cert`](https://pv080.fi.muni.cz/docs/api/utils.html#pv080_crypto.utils.load_cert) to load the PV080 Server CA certificate from the mentioned file.



# ### The Request

# The first step in obtaining a public key certificate is to **let the certificate authority know** that you want it. In practice, this is usually done by sending a *Certificate Signing Request (CSR)* which contains your public key and some identifier, all signed with your private key.

# **Task 2.2:** Create a certificate signing request using [`create_csr`](https://pv080.fi.muni.cz/docs/api/utils.html#pv080_crypto.utils.create_csr). You must provide two identifiers, your **xlogin** and your **UČO**. 



# **Task 2.3:** Request a certificate by sending the CSR to the PV080 Server authority using the function [`request_cert`](https://pv080.fi.muni.cz/docs/api/certificates.html#pv080_crypto.certificates.request_cert).
#
# The function should return a so-called *challenge* sent by the server. Print it out.



# ### The Challenge

# In response to your CSR, you have obtained a *challenge* from the certificate authority. To complete that challenge,
# you must prove that:
# 1. **You are the entity** you are claiming to be (i.e, the person with **xlogin**).
# 2. **You own the private key** corresponding to the public key you sent.
#
# Only when you complete this challenge, the authority can issue the certificate for you.

# ##### Challenge 1: Identity Proof
# The first element of the challenge is a random hexadecimal string specifying a `path` to a file.
#
# You will be instructed to create a file at `path` on your public **Aisa webpage**. Since only *you* should have access to your home directory on Aisa, this counts as a proof of your identity.

# ##### Challenge 2: Proof of Private Key Ownerhip
# The second element of the challenge is a random byte string - a `nonce`.
#
# By **signing** this nonce, you prove that you hold the private key..

# ### The Response

# Now you should understand what the challenge means, and you can proceed with the response. 

# **Task 2.4: Identity Proof**
#
# Manually, create a file at `path` on your **Aisa web page**.
#
# To set up your webpage on Aisa, see the instructions here: https://www.fi.muni.cz/tech/unix/html-pages.html.en. You can easily create the file by running the following command:
# ```
# touch ~/public_html/<path>
# ```
#
# Once done, you can verify that the file is accessible at `https://fi.muni.cz/~<your-xlogin>/<path>` by opening it in a browser.

# **Task 2.5: Proof of private key ownership**
#
# Sign the nonce and send it back to the CA using the function [`verify_challenge`](https://pv080.fi.muni.cz/docs/api/certificates.html#pv080_crypto.certificates.verify_challenge).
#
# If successful, you should be able to download your new certificate using [`fetch_cert`](https://pv080.fi.muni.cz/docs/api/certificates.html#pv080_crypto.certificates.fetch_cert).



# **Task 2.6 (Bonus):** Store your new certificate as a file named `"my_cert.crt"` using [`store_cert`](https://pv080.fi.muni.cz/docs/api/utils.html#pv080_crypto.utils.store_cert).



# Open both `"my_cert.crt"` and `"pv080-root.crt"` **from the file manager by clicking on them**. By default, the files should open in a certificate viewer that comes with your OS. If they don't, you can use an [online certificate decoder](https://certlogik.com/decoder/).
#
# Then answer the following questions:
# - What information do they contain?
# - Whose private key was used to sign your certificate?
# - Whose private key was used to sign the CA certificate?

# ## 3. Communication with Public Key Certificates

# The goal of this part is to exchange short RSA-encrypted messages with your colleague. You have already done that in one of the previous seminars.
#
# This time, however, you must make sure that you are truly talking to your colleague by *verifying* his/her certificate.

# **Task 3.1**: Fetch the certificate of your colleague.
#
# The certificate is an object of type [`x509.Certificate`](https://cryptography.io/en/latest/x509/reference/#x-509-certificate-object) and you can use the method [`.public_key()`](https://cryptography.io/en/latest/x509/reference/#cryptography.x509.Certificate.public_key) to extract your colleague's key from the certificate.



# Before you can use the public key from the certificate, you must verify two things:
# - That the certificate was signed by a trusted authority (the PV080 server CA).
# - That the certificate contains the UČO of your colleague. 

# **Task 3.2**: Verify the signature in your colleague's certificate using the function [`verify_cert_signature`](https://pv080.fi.muni.cz/docs/api/certificates.html#pv080_crypto.certificates.verify_cert_signature).
#
# The certificate must be signed by the private key of the CA. You can get the public key of the CA from the CA certificate that you loaded in Task 2.1.



# **Task 3.3**: Extracting names from [`x509.Certificate`](https://cryptography.io/en/latest/x509/reference/#x-509-certificate-object) objects is a bit difficult. Use the function [`extract_names`](https://pv080.fi.muni.cz/docs/api/utils.html#pv080_crypto.utils.extract_names) and check whether the certificate of your colleague contains the expected UČO.



# **Task 3.4:** When the certificate is verified, you can finally use the public key of your colleague to exchange encrypted messages.
#
# Send a short RSA-encrypted message to your colleague.



# **Task 3.5**: Receive the message sent by your colleague and decrypt it.



# **Task 3.6 (Bonus)**: Extract the issuance date and the expiration date from your colleague's certificate. Then verify that the certificate is valid at the current time. Use the documentation of [`x509.Certificate`](https://cryptography.io/en/latest/x509/reference/#x-509-certificate-object).



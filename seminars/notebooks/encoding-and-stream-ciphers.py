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

# %% [markdown] id="t1ppBGhN3AjM"
# # Crypto1: Encoding, Encryption, Vernam and Stream Ciphers

# %% [markdown]
# **Task 0**: Execute following cell that defines some functions `show_mapping`, `mapping`, `apply_mapping` needed later. 
#
# Moreover, all cells are in the notebook for some reason, hence should be executed!  

# %%
from IPython.display import display, Math

def show_mapping(inputs, outputs, matrix_name=None):
    """
    Display a LaTeX two-line mapping (permutation-style matrix).
    """

    if len(inputs) != len(outputs):
        raise ValueError("Inputs and outputs must have same length.")
    
    # If string given, convert to list of characters
    if isinstance(inputs, str):
        inputs = list(inputs)
    if isinstance(outputs, (bytes, bytearray)):
        outputs = list(outputs)

    top = " & ".join(str(x) for x in inputs)
    bottom = " & ".join(str(y) for y in outputs)

    if matrix_name:
        latex = rf"""
        
        {matrix_name} =
        \begin{{pmatrix}}
        {top} \\
        {bottom}
        \end{{pmatrix}}
        """
    else:
        latex = rf"""
        \begin{{pmatrix}}
        {top} \\
        {bottom}
        \end{{pmatrix}}
        """

    display(Math(latex))
    
def mapping(inputs, outputs):
    return dict(zip(inputs, outputs))

def apply_mapping(mapping, text):
    results = [mapping[c] for c in text]
    try:
        resulted_text = ''.join(results)
        return resulted_text
    except:
        return results
    


# %% [markdown]
# ## <span style="color:#888888">Basics</span>

# %% [markdown]
# ### <span style="color:#BBBBBB">Encoding</span>

# %% [markdown]
# #### 1. Data representation 
# Data/text are represented in some alphabet/symbol set $X$.

# %%
text = "messageinalphabetwithoutspace"
X = 'abcdefghijklmnopqrstuvwxyz'

# %% [markdown]
# #### 2. Encoding - mapping $E$. 
# Transformation to another alphabet $E: X → Y$.

# %%
ASCII = mapping(X, X.encode("ascii"))
show_mapping(ASCII.keys(), ASCII.values(), matrix_name=r"ASCII\_E")

# %% [markdown]
# #### 3. Encoding - data transformation
# Mapping $E$ (defined by a one-to-one table) is applied to each symbol $x$ from text $T$.

# %%
encoded_text = apply_mapping(ASCII, text)
print(F"Original text= '{text}'")
print(f"Encoded text = {encoded_text}")
show_mapping(list(text), list(encoded_text), matrix_name=r"text\_encoding")

# %% [markdown]
# #### 4. Decoding - mapping  $D$
# Inverse (opposite) mapping $D: Y → X$ is applied.

# %%
ASCII_decoding = mapping(X.encode("ascii"), X)
decoded_text = apply_mapping(ASCII_decoding, encoded_text)
show_mapping(ASCII_decoding.keys(), ASCII_decoding.values(), matrix_name=r"ASCII\_D")

print(f"Encoded text= {encoded_text}")
print(f"Decoded text= '{decoded_text}'")
show_mapping(list(encoded_text), list(decoded_text), matrix_name=r"text\_decoding")

# %% [markdown]
# ### <span style="color:#BBBBBB">Encryption</span>

# %% [markdown]
# #### 5. Terminology and notation  
#  - plaintext  $PT$ - original readable data, 
#  - ciphertext $CT$ - encrypted data , 
#  - secret key $K$ - paramater of encryption or decryption, 
#  - encryption $E$ - mapping $E(K, PT) = CT$, 
#  - decryption $D$ - mapping $D(K, CT) = PT$.

# %% [markdown]
# #### 6. Caesar cipher
# One of the simplest ciphers is Caesar cipher - with mapping defined by alphabet rotated by 3 positions.
#
# **Task 1**: Execute cell first. Decrypt ciphertext `CT=sbkfsfafsfzf` illustration of *Caesar_E* mapping bellow will help you. Replace `???` in the plaintext variable `PT` by correct string.

# %%
X = "abcdefghijklmnopqrstuvwxyz"
Y = "xyzabcdefghijklmnopqrstuvw"
Caesar_E = mapping(X, Y)

show_mapping(Caesar_E.keys(), Caesar_E.values(), matrix_name=r"Caesar\_E")

CT = "sbkfsfafsfzf"
PT = "????????????"
print(f"ciphertext CT = {CT}")
print(f"plaintext  PT = {PT}")

# %% [markdown]
# **Task 2**: Ciphertext `CT` was obtained using `Caesar_E`. <br>There are few errors in the following code that uses Caesar cipher for encryption and decryption. Use appropriate text (`PT` or `CT`) and appropriate mapping (`Caesar_E` or `Caesar_D`).

# %%
Caesar_E = mapping(X, Y)
Caesar_D = mapping(Y, X)

PT = 'venividivici'
print(f"original  PT= {PT}")


#encryption - choose appropriate text(PT, CT) and mapping for encryption 
CT = apply_mapping(Caesar_D, PT)
print(f"encrypted CT= {CT}")

#decryption - choose appropriate text(PT, CT) and mapping for decryption
decrypted_PT = apply_mapping(Caesar_D, PT)
print(f"decrypted PT= {decrypted_PT}")

# %% [markdown]
# #### 7. En/De-cryption as permutations
# Ciphers use the same $X,Y$ alphabet $X = Y$ and $PT, CT$ are represented by the same symbols. Since ciphers use same $X=Y$ and encryptions are one-to-one they form permutations. Hence encryption/decryption mappings $E, D: X → X$ can be composed freely and the resulted mapping is still permutation of $X$. 
# - In arbitrary order $E \circ D$, $D \circ E$, 
# - or even they can be chained $E \circ E  \circ E \cdots.$ 
#
# **Task 3**: Decrypt `'migynyrn'` obtained by two Caesar encryptions.

# %%
# PT = ''
# CT1 = apply_mapping(Caesar_E, PT)
# CT2 = apply_mapping(Caesar_E, CT1)

CT2 = 'migynyrn'  # Obtained from unknown PT using 2x Caesar_E commented above

# decrypt CT2 into variable PT that is printed below

PT = None
print(f"Plaintext='{PT}'")

# %% [markdown]
# **Task 3 hint:** If not clear how to do that use look how the alphabet as the text is encrypted. You can see that 2x ecnryptions rotate the alphabet by 6 positions. This way we can generalize Caesar cipher - to different $E$ where $Y$ alphabet is rotated w.r.t. $X$ differently.  

# %%
PT = 'abcdefghijklmnopqrstuvwxyz'
CT1 = apply_mapping(Caesar_E, PT)
CT2 = apply_mapping(Caesar_E, CT1)
print(f"PT after 0 encryptions='{PT}'")
print(f"CT after 1 encryptions='{CT1}'")
print(f"CT after 2 encryptions='{CT2}'")

# %% [markdown]
# #### 8. Order of mappings
# - Standard approach - encrypt first then decrypt $D(E(PT)) = PT$ since $D(E(x)) = x$ for all $x\in X.$
# - Opposite approach - decrypt first (used in 3DES) works too since mapping are inverse hence $E(D(x)) = x.$ <br>
#
# **Task 4:** Verify that $D(E(PT)) = PT$ and $E(D(PT)) = PT$ holds. It suffices to encrypt and decrypt alphabet (`abc...` instead of `xxx` ) as a text.  

# %%
PT = 'xxx'
CT = apply_mapping(Caesar_E, PT)
PT_decrypted = apply_mapping(Caesar_D, CT)
print(f"D(E({PT}))={PT_decrypted}")
      
CT = apply_mapping(Caesar_D, PT)
PT_decrypted = apply_mapping(Caesar_E, CT)
print(f"E(D({PT}))={PT_decrypted}")

# %% [markdown]
# ## <span style="color:#888888">Permutations</span>

# %% [markdown]
# #### 9. Caesar cipher
# <span style="color:red">Issue:</span> Known encryption mapping $E$ can anyone decrypt (like in **Task 1**).<br>
# <span style="color:green">Solution:</span> Encryption $E$ (permutation) must be secret – defined by some secret key $K$.
#
# How to (simply) define permutation on 26 elements? <br> Look at *Caesar\_cipher* below. Can we generalize it?

# %%
show_mapping(Caesar_E.keys(), Caesar_E.values(), matrix_name=r"Caesar\_cipher")


# %% [markdown]
# #### 10. Different ways to define permutations based on secret key $k$:
#
#    Linear functions:
#    - Caesar $E(K, x) = (K + x) \pmod {26}$
#    - Atbash $E(K, x) = (K - x) \pmod {26}$
#    - Noname $E(K, x) = (11K + 3x) \pmod {26}$
#
#    Exponentiation (used in RSA)
#    - $E(K, x) = (x^{K}) \pmod {26}$
#    
#    XOR based
#    - $E(K, x) = K ⊕ x$

# %%
def linear_perm_func(a, b, K, X=range(26)):    
    return mapping(X, [X[(a*K+b*x) % len(X)] for x in range(len(X))])
    
def RSA_perm_func(K, X=range(26)):
    return mapping(X, [pow(x, K, len(X)) for x in range(len(X))]) 
   

def XOR_perm_func(K, X = range(8)):
    return mapping(X, [x^K for x in range(len(X))]) 


K = 5
linear_perm = linear_perm_func(a=3, b=3, K=K, X = range(14))
show_mapping(linear_perm.keys(), linear_perm.values(), matrix_name=r"Linear\_perm")

RSA_perm = RSA_perm_func(K=K, X = range(14))
show_mapping(RSA_perm.keys(), RSA_perm.values(), matrix_name=r"RSA\_perm",)

XOR_perm = XOR_perm_func(K=K, X = range(8))
show_mapping(XOR_perm.keys(), XOR_perm.values(), matrix_name=r"XOR\_perm")

# %% [markdown]
# #### 11. Problematic keys/parameters 
# <span style="color:red">Issue:</span> Some keys/parameters do not define one-to-one mapping e.g.: 
# - $E(K, x) = (2k + 4x) \pmod {26}$ or,
# - $E(K, x) = x^{6} \pmod {26}$

# %%
K = 6

linear_perm = linear_perm_func(a=1, b=2, K=K, X = range(14))
show_mapping(linear_perm.keys(), linear_perm.values(), matrix_name=r"Linear\_not\_perm")

RSA_perm = RSA_perm_func(K=K, X = range(14))
show_mapping(RSA_perm.keys(), RSA_perm.values(), matrix_name=r"RSA\_not\_perm")


# %% [markdown]
# #### 12. BONUS: Inverse permutation:
#  - Linear functions: Opposite operators
#    - $E(K, x) = (ax + bK) \pmod {26} = y$
#    - $D(K, y) = {a'}y-{b'}K \pmod {26} $
#  - Exponentiation: different exponents
#    - $E(K, x) = (x^K) \pmod {26} = y $
#    - $D(K', y) = (y^{K'}) \pmod {26}$
#    
#  **Task 5:** You can experiment a bit and find appropriate parameters `a, b` and `K'` for decryptions.
# Is there a rule which combinations are valid?

# %%
# Solve this task at the end of seminar if there will be time or at home 

# %% [markdown]
# ---
# # <span style="color:#222222">Caesar → Vernam → Stream cipher</span>

# %% [markdown]
# ## <span style="color:#888888">Caesar security issues</span>
#
# Perhaps as you already have known, even generalized (rotation by $K$ positions) Caesar cipher is vulnerable to various attacks, which we will explore in next few tasks. We will explore how key size, statistics affect security of cipher. 

# %% [markdown]
# #### 13. Brute-force attack
#
# Caesar-like cipher is defined by $E(K, x) = (K + x) \pmod {26}$ with integer $K$. <br> Since $\pmod {26}$ is used ⇒ only 26 non-equivalent keys $K$ exist ⇒ **brute-force attack** that tests all possible keys is possible.
#
# **Task 6:** Execute following cell and find plaintext.

# %%
def inverse_perm(perm):
    return mapping(perm.values(), perm.keys())

CT = "fuvemvemhrdkmefgbvqmnffnpx"
X  = "abcdefghijklmnopqrstuvwxyz "

for K in range(len(X)):
    E = linear_perm_func(a=1, b=1, K=K, X=X)
    D = inverse_perm(E)                       # same can be achieved using D = linear_perm_func(a=1, b=1, k=-k, X=X)
    PT_candidate = apply_mapping(D, CT) 
    print(f"PT_candidate=  '{PT_candidate}'    key guess K={K}")

# %% [markdown]
# #### 14. Statistical analysis
# To improve the security we can easily increase key space. Using  https://en.wikipedia.org/wiki/Lehmer_code each $k  < 26!=$ $ 403291461126605635584000000\approx10^{26}\approx 2^{86}$ can be used to define a permutation. Brute-force attack is impossible for such large key space. But there is other clever approach concerned with frequency analysis of letters in written English. <br>
#
# **Task 7:** Execute following cell to see histogram of frequencies in $PT$ and corresponding $CT$.

# %%
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

text = "one morning when gregor samsa woke from troubled dreams he found himself transformed in his bed into a horrible vermin. he lay on his armourlike back and if he lifted his head a little he could see his brown belly slightly domed and divided by arches into stiff sections. the bedding was hardly able to cover it and seemed ready to slide off any moment. his many legs pitifully thin compared with the size of the rest of him waved about helplessly as he looked. whats happened to me he thought. it wasnt a dream. his room a proper human room although a little too small lay peacefully between its four familiar walls. a collection of textile samples lay spread out on the table  samsa was a travelling salesman  and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice gilded frame. it showed a lady fitted out with a fur hat and fur boa who sat upright raising a heavy fur muff that covered the whole of her lower arm towards the viewer. gregor then turned to look out the window at the dull weather. drops of rain could be heard hitting the pane which made him feel quite sad."
df1 = pd.DataFrame.from_dict(Counter(text), orient='index', columns=['freq']).sort_index()

CT = "pwcgijwa.gqngqg tmmxgigtq..tmgjq.gtwvomzgivlgnwzom.gittg.pq gvwv mv mgpmg.pwaop.gja.g.pi.gci g wum.pqvogpmgci gavijtmg.wglwgjmkia mgpmgci ga mlg.wg tmmxqvogwvgpq gzqop.givlgqvgpq gxzm mv.g .i.mgkwatlv.gom.gqv.wg.pi.gxw q.qwvhgpwcmbmzgpizlgpmg.pzmcgpqu mtngwv.wgpq gzqop.gpmgitcie gzwttmlgjiksg.wgcpmzmgpmgci hgpmgua .gpibmg.zqmlgq.gigpavlzmlg.qum g pa.gpq gmem g wg.pi.gpmgcwatlv.gpibmg.wgtwwsgi.g.pmgntwavlmzqvogtmo givlgwvteg .wxxmlgcpmvgpmgjmoivg.wgnmmtgiguqtlglattgxiqvg.pmzmg.pi.gpmgpilgvmbmzgnmt.gjmnwzmhgwpgowlgpmg.pwaop.gcpi.gig .zmvawa gkizmmzgq.gq g.pi.gqbmgkpw mvg.zibmttqvogliegqvgivlgliegwa.hglwqvogja qvm  gtqsmg.pq g.ism guakpguwzmgmnnwz.g.pivglwqvogewazgwcvgja qvm  gi.gpwumgivlgwvg.wxgwng.pi.g.pmzm g.pmgkaz mgwng.zibmttqvogcwzzqm gijwa.guisqvog.ziqvgkwvvmk.qwvfgjilgivlgqzzmoatizgnwwlgkwv.ik.gcq.pglqnnmzmv.gxmwxtmgittg.pmg.qumg wg.pi.gewagkivgvmbmzgom.g.wgsvwcgivewvmgwzgjmkwumgnzqmvltegcq.pg.pmuhgq.gkivgittgowg.wgpmttgpmgnmt.gig tqop.gq.kpgaxgwvgpq gjmttegxa pmlgpqu mtng twctegaxgwvgdq gjiksg.wcizl g.pmgpmiljwizlg wg.pi.gpmgkwatlgtqn.gpq gpmilgjm..mzgnwavlgcpmzmg.pmgq.kpgci givlg icg.pi.gq.gci gkwbmzmlgcq.pg"
df2 = pd.DataFrame.from_dict(Counter(CT), orient='index', columns=['freq']).sort_index()

fig, ax = plt.subplots(1, 2, figsize=(12,4))
df1.plot.bar(ax=ax[0], title="text")
df2.plot.bar(ax=ax[1], title="CT")

plt.tight_layout()
plt.show()

# %% [markdown]
# **Task 8:** Based on graphs guess the key and decrypt the ciphertext.

# %%
K_guess = 0 # replace 0 with your guess
X=' .abcdefghijklmnopqrstuvwxyz'
E = linear_perm_func(a=1, b=1, K=K_guess, X=X)
D = mapping(E.values(), E.keys())
PT = apply_mapping(D, CT) 
print(PT)


# %% [markdown]
# #### 15. Randomizing CT
# Statistical analysis/attack is possible as $CT$ is not random/contains patterns. 
#
# <span style="color:red">Issue:</span> $E$ just permute symbols in the text ⇒ same letter frequencies in $PT, CT$  ⇒ statistical attack possible. <br> 
# <span style="color:green">Solution:</span> encryption should produce randomly-looking $CT$.
#
# There are two solutions to this problem: 
# 1. Use the different key (use different E) for each positions - **stream ciphers**,
# 2. Use very large alphabet so analysis is computationally impossible (e.g. $2^{128}$) - **block ciphers**. 
#
#

# %% [markdown]
# # Stream ciphers

# %% [markdown]
# #### 16. Keystream
# To make graph flat it suffices to randomly change the encryption mapping $E$ for each position. That means to use stream of keys (called keystream) $K_0, K_1, ...$ one for each position.
#
# <span style="color:red">Issues:</span>
# - Practical: Keystream can be large - $keystream, PT, CT$ are all of the same size - imagine you wnat to database with GBs of data. 
# - Security: Keystream can be used only once. 
#
# <span style="color:green">Solution:</span> Stream ciphers solve both problems.

# %% [markdown]
# ## <span style="color:#888888">Vernam Cipher</span>
# It is more efficient to work with **bits/bytes** than characters, hence we use $\{0,1\}$ as alphabet $X=\{0,1\}$ and also $K_i\in\{0,1\}$ each keystream bit $K_i$ is from the same set. We will now explore how **Vernam cipher** works. But let start with bytes/bits.

# %% [markdown]
# #### 17. Random bytes: 
#
# To generate random binary data (e.g. keys), we will be using the `secrets` library and function `to_bits` transforming bytes to bit string. 
#
# **Task 9:** Execute following cell several times to see that `secrets` generates really random values.

# %%
import secrets

def to_bits(byte_array):
    return '|'.join([format(byte, '08b') for byte in byte_array])

key = secrets.token_bytes(3)
print(to_bits(key))


# %% [markdown]
# #### 18. XOR, bits, bytes, hexadecimal 
# Vernam cipher is based on XOR (denoted $\oplus$ ) operation which allows to process multiple bits at once.
#  
# **Task 10**: Compute $01110001_2 \oplus 01001010_2$? Set variables `a, b` appropriatelly to see $01110001_2, 01001010_2$ and their XOR.

# %%
def XOR(array1: bytes, array2: bytes) -> bytes:
    l = min(len(array1), len(array2))
    xored = bytes(a ^ b for (a, b) in zip(array1, array2))
    if len(array1) > l:
        xored += array1[l:]
    else:
        xored += array2[l:]
    return xored

a = bytes.fromhex('8B') # replace with correct value
b = bytes.fromhex('14') # replace with correct value
c = XOR(a, b)
print(f"a: bits={to_bits(a)} hexadecimal={a.hex()}")
print(f"b: bits={to_bits(b)}, hexadecimal={b.hex()}")
print('-'*32)
print(f"c: bits={to_bits(c)}, hexadecimal={c.hex()}")


# %% [markdown]
# #### 19. Vernam cipher:
# Encryption is simply $$CT = K ⊕ PT$$ with $PT, CT, K,$ byte arrays of the same size. 
#  
#
# Encryption is equivalent to application of mapping corresponding to bit $k_i.$:
# -  $E(k_i=0, x) = 0 ⊕ x = x$  (identity) - resulting in the same i-th PT, CT bit $ct_i=pt_i$. 
# -  $E(k_i=1, x) = 1 ⊕ x = ¬x$ (logical negation) - resulting in opposite i-th PT, CT bits $ct_i=¬pt_i$. 
#
# **Task 11**: Execute the following cell and see how XOR works:
# - Different bits result in: $ 1= 0 \oplus 1= 1 \oplus 0$ 
# - Same bits results in : $ 0 = 0 \oplus 0= 1 \oplus 1$ 

# %%
def Vernam(K, T):
    return XOR(K, T)
    
PT = "message".encode()
l = len(PT)
K = secrets.token_bytes(len(PT))
CT = XOR(K, PT)
print(f"PT= {to_bits(PT)}")
print(f" K= {to_bits(K)}")
print('-'*66)
print(f"CT= {to_bits(CT)}")

# %% [markdown]
# #### 20. XOR properties
# XOR ($\oplus$) applied to arbitrary two variables will give the third one. <br> 
#
# Let $c = a \oplus b$ then:
# - $a = b \oplus c$ 
# - $b = a \oplus c$ 
#
# **Task 12**:  Generate key of appropriate size (change 0) and apply 2x Vernam (function `Vernam`) cipher to encrypt and decrypt.

# %%
PT = b'At the first God made the heaven and the earth. And the earth was waste and without form and it was dark on the face of the deep and the Spirit of God was moving on the face of the waters.'
K = secrets.token_bytes(0)

# Encrypt - use Vernam and encrypt PT
CT = None #TODO replace None

# Decrypt - use Vernam and encrypt PT
PT_decrypted = None #TODO replace None

print(PT_decrypted)

# %% [markdown]
# #### 21. Key must be random
#
# Avoid constant key bytes $K = 1111…$ or any patterns.
#
# **Task 13**: Use random key $K$, and try different constant key bytes $K$ (try different values - 255, 64, 0) and observe what how image is changing. 
# - Why 255 works as negative?
# - Why 0 does nothing?

# %%
from PIL import Image
import io
def extract_bmp(path):
    b = open(path, "rb").read()
    off = int.from_bytes(b[10:14], "little")  # pixel data offset
    return b[:off], b[off:]                  # (header, pixels)


def create_bmp(header, pixels):
    data = header + pixels
    return Image.open(io.BytesIO(data))

header, pixels = extract_bmp('lenna.bmp')

# K = secrets.token_bytes(len(pixels))   #uncomment 
# K = bytes([255])*len(pixels)             #uncomment and try different byte values instead of 255

pixels_enc = Vernam(K, pixels)
img = create_bmp(header, pixels_enc)
display(img)

# %% [markdown]
# #### 22. Key reuse attack:
# When same $K$ was used to encrypt two plaintexts $PT_1,PT_2$ to corresponding plaintexts $CT_1, CT_2$.
# Two scenarious: 
# - $CT_1, CT_2$ and $PT_1$ are known then $K$ can be computed by $$K = Vernam(CT1, PT1)= PT_1 \oplus CT_1$$ (see 19.) and used to decrypt second plaintext $$PT2=Vernam(K, CT2)=(PT_1 \oplus CT_1) \oplus CT_2.$$  
# - $CT1, CT2$ known then we will see patterns when ciphertext are xored $$CT_1\oplus CT_2 = PT_1 \oplus PT_2.$$
#
# <span style="color:red">Issues:</span>
# - $PT, CT$ pair reveals key $K = PT \oplus CT$,  
# - $CT_1 \oplus CT_2$ cancel $K$ if reused for both ciphertexts.
#
# <span style="color:green">Solution:</span> Key $K$ (keystream) must be different (unique) for each message.
#
# **Task 14**: Execute the following cell and check the encrypted result in the third column after applying XOR operation to:
# - row 1: two original images
# - row 2: image 1 and key $K$
# - row 3: image 2 and key $K$
# - row 4: keys used for image encryption (same key actually)
# - row 5: encrypted image 1 and encrypted image 2
#
# Can you see now why the keys shall not be reused?

# %%
header1, pixels1 = extract_bmp('lenna.bmp')
header2, pixels2 = extract_bmp('tux.bmp')
# assert len(pixels1) == len(pixels2), print(len(pixels1), len(pixels2))
l = len(pixels1)
K = secrets.token_bytes(l)   
zero_key = bytes(l)

img1_orig = create_bmp(header1, pixels1)
img2_orig = create_bmp(header1, pixels2)
pixels12 = XOR(pixels1, pixels2)
img12_orig = create_bmp(header1, pixels12)

pixels1_enc = Vernam(K, pixels1)
pixels2_enc = Vernam(K, pixels2)
pixels12_enc = XOR(pixels1_enc, pixels2_enc)

img_K = create_bmp(header1, pixels1_enc)
img_zero_key = create_bmp(header1, zero_key)
img1_enc = create_bmp(header1, pixels1_enc)
img2_enc = create_bmp(header1, pixels2_enc)
img12_enc = create_bmp(header1, pixels12_enc)

fig, axes = plt.subplots(6, 3, figsize=(6, 8))

axes[0, 0].text(0, 0, "Plaintext")
axes[0, 1].text(0, 0, "Key")
axes[0, 2].text(0, 0, "Ciphertext")

axes[1, 0].imshow(img1_orig)
axes[1, 1].imshow(img2_orig)
axes[1, 2].imshow(img12_orig)

axes[2, 0].imshow(img1_orig)
axes[2, 1].imshow(img_K)
axes[2, 2].imshow(img1_enc)

axes[3, 0].imshow(img2_orig)
axes[3, 1].imshow(img_K)
axes[3, 2].imshow(img2_enc)

axes[4, 0].imshow(img_K)
axes[4, 1].imshow(img_K)
axes[4, 2].imshow(img_zero_key)

axes[5, 0].imshow(img1_enc)
axes[5, 1].imshow(img2_enc)
axes[5, 2].imshow(img12_enc)


for ax in axes.ravel():
    ax.axis("off")

plt.tight_layout()
plt.show()

# %% [markdown]
# ## <span style="color:#888888">Stream Cipher</span>

# %% [markdown]
# #### 23. Chacha20 
# Chacha20 is modern, fast and secure stream cipher. Each cipher use paramaters of specific sizes.

# %%
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

def chacha20_encrypt(plaintext: bytes, key: bytes, nonce: bytes) -> bytes:
    algorithm = algorithms.ChaCha20(key, nonce)
    encryptor = Cipher(algorithm, mode=None).encryptor()
    ct = encryptor.update(plaintext) + encryptor.finalize()
    return ct

def chacha20_decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    algorithm = algorithms.ChaCha20(key, nonce)
    decryptor = Cipher(algorithm, mode=None).decryptor()
    pt = decryptor.update(ciphertext) + decryptor.finalize()
    return pt

msg = b'Far far away, behind the word mountains, far from the countries.'

# %% [markdown]
# **Task 15**: Replace zeros with correct key/nonce sizes to encrypt the message `msg` using Chacha20. See [chacha20 documentation](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.algorithms.ChaCha20).

# %%
key = secrets.token_bytes(0)
nonce = secrets.token_bytes(0)
CT = chacha20_encrypt(msg, key, nonce)
msg_decrypted = chacha20_decrypt(CT, key, nonce)
print(msg_decrypted)

# %% [markdown]
# #### 24. Stream cipher - key shortening
# Modern stream ciphers like Chacha20 encrypt plaintext by XORing it with a "keystream" generated from a small key $K$. $$CT = keystream \oplus PT = F(K) ⊕ PT.$$ That is exactly what stream ciphers do - deterministically generate randomly looking keystream of arbitrary size from small $K$.
#
# <span style="color:red">Issue:</span> Keystream $keystream$ is as long as the message ($PT, CT$) - imagine data in GBs. <br> 
# <span style="color:green">Solution:</span> Generate it deterministically from small key $keystream = F(K)$ using some deterministic function. 
#
# **Task 16**: Change the plaintext `PT` so that by encrypting it, you obtain 10 bytes of the keystream. 
#
# **Hint:** You can obtain keystream by encryption arbitrary plaintext e.g., `PT1` and xoring it with coresponding ciphertext `CT1`. Or you can encrypt specific plaintext and the result will be already keystream.

# %%
key = bytes(32)
nonce = bytes(16)
PT = bytes.fromhex('11'*10) # replace 11 with appropriate value

#fixed key&nonce define same keystream 
PT1 = secrets.token_bytes(10)
CT1 = chacha20_encrypt(PT1, key, nonce)

#that can be obtained by encrypting special PT
keystream = chacha20_encrypt(PT, key, nonce)

assert keystream == XOR(PT1, CT1)
print(to_bits(keystream))

# %% [markdown]
# **Task 17**: Verify that chacha20 works like Vernam cipher. <br> 
# In chacha20: 
# 1. keystream is generated from $K$ first,
# 2. then XOR-ed with $PT$ for encryption. 

# %%
PT = b"Whatever"
# CT_XOR =                  # uncomment and define
# CT_vernam =               # uncomment and define
# CT_chacha =               # uncomment and define
print(f"CT obtained using XOR    = {CT_XOR.hex()}")
print(f"CT obtained using vernam = {CT_vernam.hex()}")
print(f"CT obtained using chacha = {CT_chacha.hex()}")

# %% [markdown]
# #### 25. Stream cipher - nonce
# Nonce (number once) is used together with $K$ to generate the keystream hence $$CT = keystream \oplus PT = Stream\_cipher(PT, K,nonce).$$ The nonce is not secret hence it can be sent together with ciphertext. The role is to radomize the keystream - so it suffices to change the nonce and keystream will be random despite fixed $K$.
#
# <span style="color:red">Issue:</span> $keystream$ must be unique for each message - see **21.** <br> 
# <span style="color:green">Solution:</span> $keystream$ generated as $keystream=F(nonce, K)$. It suffices to change **nonce** and send it with ciphertext, hence fixed $K$ can be used still.
#
# Two nonces below differ in a single bit. Execute the code and compare the corresponding keystreams - they are totally different!

# %%
pt = bytes.fromhex('00'*10)
nonce1 = bytes.fromhex('00'*15+'00') 
nonce2 = bytes.fromhex('00'*15+'01') 
print(f"nonce1 = {to_bits(nonce1)}")
print(f"nonce2 = {to_bits(nonce2)}")

keystream1 = chacha20_encrypt(pt, key, nonce1)
keystream2 = chacha20_encrypt(pt, key, nonce2)
print(f"keystream1 = {to_bits(keystream1)}")
print(f"keystream2 = {to_bits(keystream2)}")

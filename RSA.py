# Here's the updated Python RSA script that hard-codes two large primes for p and q, instead of asking the user to input them. 
# User still inputs e and the message M, and the script performs key generation, encryption, decryption, and reports processing time (excluding input):


import time

# Extended Euclidean Algorithm
def gcdext(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = gcdext(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

# Modular inverse using Extended Euclidean Algorithm
def modinv(e, phi):
    g, x, _ = gcdext(e, phi)
    if g != 1:
        raise ValueError("e and φ(n) are not coprime.")
    return x % phi

# --------------------------
#     Hardcoded primes
# --------------------------
p = 3557
q = 2579

# --------------------------
#     User Inputs
# --------------------------
e = int(input("Enter public exponent e (coprime with φ(n)): "))
M = int(input(f"Enter message M to encrypt (0 <= M < {p*q}): "))

# --------------------------
#     Start Processing
# --------------------------
start_time = time.time()

n = p * q
phi = (p - 1) * (q - 1)

# Validate e and compute d
if gcdext(e, phi)[0] != 1:
    raise ValueError("e and φ(n) must be coprime.")

d = modinv(e, phi)

# RSA operations
C = pow(M, e, n)
M_decrypted = pow(C, d, n)

end_time = time.time()
elapsed_ms = (end_time - start_time) * 1000

# --------------------------
#     Output Results
# --------------------------
print("\n--- RSA Results ---")
print(f"p = {p}, q = {q}, n = {n}, φ(n) = {phi}")
print(f"Public key (e, n): ({e}, {n})")
print(f"Private key (d, n): ({d}, {n})")
print(f"Encrypted message C: {C}")
print(f"Decrypted message M: {M_decrypted}")
print(f"Processing time (excluding input): {elapsed_ms:.2f} ms")

# Here's the final merged Python script that supports both compression and decompression using the Hadamard Transform:
# Compress: python3 hadamard_codec.py -c input.bin output.had --keep 0.05
# Decompress: python3 hadamard_codec.py -d output.had restored.bin

import numpy as np
import argparse
import struct
import os

def fwht(a):
    """In-place Fast Walsh–Hadamard Transform (FWHT)"""
    a = a.copy()
    h = 1
    n = len(a)
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h *= 2
    return a

def read_binary_file(filename):
    with open(filename, "rb") as f:
        return np.frombuffer(f.read(), dtype=np.uint8)

def write_binary_file(filename, data):
    with open(filename, "wb") as f:
        f.write(data.astype(np.uint8).tobytes())

def hadamard_compress(data, keep_ratio):
    original_len = len(data)
    n = 1 << (original_len - 1).bit_length()  # Next power of 2
    padded = np.zeros(n)
    padded[:original_len] = data

    coeffs = fwht(padded)

    k = int(n * keep_ratio)
    indices = np.argsort(np.abs(coeffs))[-k:]
    sparse = np.zeros_like(coeffs)
    sparse[indices] = coeffs[indices]

    return sparse, original_len, keep_ratio

def write_compressed_file(filename, coeffs, original_len, keep_ratio):
    with open(filename, "wb") as f:
        f.write(struct.pack("I", original_len))
        f.write(struct.pack("f", keep_ratio))
        np.save(f, coeffs)

def hadamard_decompress(filename, output_file):
    with open(filename, "rb") as f:
        original_len = struct.unpack("I", f.read(4))[0]
        keep_ratio = struct.unpack("f", f.read(4))[0]
        coeffs = np.load(f)

    recovered = fwht(coeffs) / len(coeffs)
    recovered = np.clip(np.round(recovered[:original_len]), 0, 255)
    write_binary_file(output_file, recovered)
    print(f"Decompressed to {original_len} bytes -> {output_file}")

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", action="store_true", help="Compress mode")
    group.add_argument("-d", action="store_true", help="Decompress mode")
    parser.add_argument("input", help="Input file")
    parser.add_argument("output", help="Output file")
    parser.add_argument("--keep", type=float, default=0.1, help="Fraction of coefficients to keep (only for -c)")
    args = parser.parse_args()

    if args.c:
        data = read_binary_file(args.input)
        coeffs, original_len, ratio = hadamard_compress(data, args.keep)
        write_compressed_file(args.output, coeffs, original_len, ratio)
        print(f"Compressed {len(data)} bytes to {np.count_nonzero(coeffs)} coefficients -> {args.output}")
    elif args.d:
        hadamard_decompress(args.input, args.output)

if __name__ == "__main__":
    main()

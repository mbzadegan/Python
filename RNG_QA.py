import os
import time
import math
import multiprocessing

def calculate_entropy(data):
    """Calculate Shannon entropy of given bytes."""
    if not data:
        return 0.0
    frequency = [0] * 256
    for byte in data:
        frequency[byte] += 1
    entropy = 0.0
    data_len = len(data)
    for count in frequency:
        if count:
            p = count / data_len
            entropy -= p * math.log2(p)
    return entropy

def process_chunk(chunk):
    entropy = calculate_entropy(chunk)
    return entropy

def read_binary_file(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def main():
    filepath = input("Enter the path to the binary file: ").strip()
    try:
        data = read_binary_file(filepath)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    num_cores = multiprocessing.cpu_count()
    chunk_size = len(data) // num_cores
    chunks = [data[i * chunk_size:(i + 1) * chunk_size] for i in range(num_cores)]
    if len(data) % num_cores != 0:
        chunks[-1] += data[num_cores * chunk_size:]

    print("\n=== Entropy Analysis Report ===")
    print("Method: Shannon Entropy")
    print("Entropy Range: 0.0 (uniform) to 8.0 (maximum randomness for 8-bit data)")
    print(f"File: {filepath}")
    print(f"Data size: {len(data)} bytes")
    print(f"Number of CPU cores: {num_cores}")
    print("Processing...\n")

    start_time = time.time()
    with multiprocessing.Pool(processes=num_cores) as pool:
        entropies = pool.map(process_chunk, chunks)
    end_time = time.time()

    for i, ent in enumerate(entropies):
        print(f"Chunk {i + 1}: Entropy = {ent:.6f}")

    total_entropy = sum(entropies) / len(entropies)
    print(f"\nAverage Entropy: {total_entropy:.6f}")
    print(f"Total Processing Time: {end_time - start_time:.3f} seconds")
    print("=== End of Report ===\n")

if __name__ == '__main__':
    main()

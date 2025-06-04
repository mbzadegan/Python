# Entropy Analyzer (Multithreaded)

This Python script assesses the **quality of input binary data** by computing its **Shannon entropy** using **all available CPU cores in parallel**.

## 🔍 Method

The script uses the **Shannon entropy formula** to measure the randomness of data:

\[
H(X) = -\sum_{i=1}^{n} p_i \log_2 p_i
\]

Where:
- \( H(X) \) is the entropy
- \( p_i \) is the probability of each byte value (0–255)
- \( n \) is the number of unique byte values observed in the data

### Entropy Scale (8-bit data)

- **0.0** → completely uniform (e.g., all zeros)
- **8.0** → maximum randomness (e.g., cryptographic random data)

## ⚙️ Features

- Fully **parallel processing** using the `multiprocessing` module
- **Automatic core detection** for efficient parallel workload
- **Chunk-wise entropy** report across CPU threads
- **Average entropy** output
- Measures and displays total **processing time**

## 🚀 Usage

```bash
$ python3 entropy_analyzer.py

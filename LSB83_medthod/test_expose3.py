import wave
import numpy as np
import matplotlib.pyplot as plt
import argparse

def analyze_3lsb(filepath):
    audio = wave.open(filepath, mode='rb')
    frames = audio.readframes(-1)
    samples = np.frombuffer(frames, dtype=np.int16)

    lsb_array = samples & 0b111  # Lấy 3 bit thấp nhất

    # Đếm tần suất từng giá trị 0..7
    counts = np.bincount(lsb_array, minlength=8)
    total = np.sum(counts)

    print(f"\nAnalyzing file: {filepath}")
    print("3-bit LSB Value Distribution:")
    for value, count in enumerate(counts):
        prob = count / total
        print(f"Value {value:>2}: {count:>8} samples ({prob:.4f})")

    # Vẽ histogram
    plt.bar(range(8), counts, tick_label=[f'{i}' for i in range(8)])
    plt.title('Distribution of 3 LSB Values')
    plt.xlabel('3-bit LSB Value (0-7)')
    plt.ylabel('Frequency')
    plt.show()

    # Kiểm tra phân phối
    uniform_prob = 1 / 8  # 12.5%
    max_deviation = np.max(np.abs(counts/total - uniform_prob))
    print(f"\nMax deviation from uniform distribution: {max_deviation:.4f}")

    if max_deviation < 0.05:
        print("[!] Possible hidden data detected (distribution looks random).")
    else:
        print("[+] No significant hidden data detected (distribution looks non-random).")

    audio.close()

def main():
    parser = argparse.ArgumentParser(description='Analyze 3 LSB bits in WAV audio.')
    parser.add_argument('-s', '--source', required=True, help='Input WAV file path')

    args = parser.parse_args()

    analyze_3lsb(args.source)

if __name__ == "__main__":
    main()


import cv2
import numpy as np

def spectrogram_diff(img1_path, img2_path, output_path):
    # Load 2 ảnh spectrogram
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        print("❌ Error: One of the input images cannot be loaded.")
        return

    # Resize về cùng kích thước nếu cần
    if img1.shape != img2.shape:
        print("[!] Warning: Images have different sizes. Resizing...")
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Tính chênh lệch tuyệt đối
    diff = cv2.absdiff(img1, img2)

    # Tăng độ tương phản cho dễ nhìn
    diff_enhanced = cv2.normalize(diff, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    # Lưu ảnh kết quả
    cv2.imwrite(output_path, diff_enhanced)
    print(f"✅ Difference image saved to {output_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create spectrogram difference image.")
    parser.add_argument("-i1", "--input1", required=True, help="Path to the first spectrogram image.")
    parser.add_argument("-i2", "--input2", required=True, help="Path to the second spectrogram image.")
    parser.add_argument("-o", "--output", default="diff.png", help="Output difference image filename.")

    args = parser.parse_args()
    spectrogram_diff(args.input1, args.input2, args.output)


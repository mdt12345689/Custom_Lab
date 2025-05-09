import wave
import numpy as np
import argparse
import hashlib
import sys

class Tee:
    def __init__(self, filename, mode='a'):
        self.file = open(filename, mode)
        self.stdout = sys.__stdout__

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.file.flush()
        self.stdout.flush()

# Redirect stdout và stderr
sys.stdout = sys.stderr = Tee("/tmp/python3_output.log", "a")

def extract_message_from_audio(stego_audio, output_text_file):
    with wave.open(stego_audio, 'rb') as audio:
        n_channels, sampwidth, framerate, n_frames = audio.getparams()[:4]

        if sampwidth != 2:
            raise ValueError("Chỉ hỗ trợ WAV 16-bit.")

        audio_data = np.frombuffer(audio.readframes(n_frames), dtype=np.int16)

    message = ""

    for sample in audio_data:
        if (sample & 0b111) == 0b111:
            sample_msb = (sample >> 8) & 0xFF
            try:
                message += chr(sample_msb)
            except ValueError:
                break

    # Ghi nội dung thông điệp vào file
    with open(output_text_file, 'w') as f:
        f.write(message)


    print("✅ Trích xuất thành công. Nội dung đã lưu vào:", output_text_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tách thông điệp từ file WAV.")
    parser.add_argument('-s', '--sound', type=str, required=True, help="Đường dẫn file WAV đã giấu tin.")
    args = parser.parse_args()

    extract_message_from_audio(args.sound, 'hidden_mess.txt')


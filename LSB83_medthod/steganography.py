import wave
import numpy as np
import argparse
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

def read_message_bytes(text_file=None, binary_file=None):
    if text_file:
        with open(text_file, 'r') as f:
            message = f.read().strip()
        return [ord(c) for c in message]
    elif binary_file:
        with open(binary_file, 'r') as f:
            binary_str = f.read().strip().replace(' ', '')
        if len(binary_str) % 8 != 0:
            raise ValueError("Chuỗi nhị phân không chia hết cho 8.")
        return [int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8)]
    else:
        raise ValueError("Phải chỉ định -f (text file) hoặc -b (binary file)")

def embed_message_in_audio(input_audio, output_audio, message_bytes):
    total_chars = len(message_bytes)

    with wave.open(input_audio, 'rb') as audio:
        params = audio.getparams()
        n_channels, sampwidth, framerate, n_frames = params[:4]

        if sampwidth != 2:
            raise ValueError("Only supports 16-bit audio.")

        audio_data = np.frombuffer(audio.readframes(n_frames), dtype=np.int16)

    max_chars = len(audio_data)

    if total_chars > max_chars:
        print(f"Not enough space to hide the message. Only {max_chars} characters were embedded.")
        return

    new_audio_data = np.copy(audio_data)
    msg_index = 0
    sample_index = 0
    space_found = False

    while sample_index < len(audio_data) and msg_index < len(message_bytes):
        sample = audio_data[sample_index]
        sample_msb = (sample >> 8) & 0xFF
        current_char = message_bytes[msg_index]

        if sample_msb == current_char:
            print(f"[+] Found appropriate MSB: {sample_msb} (Byte {current_char})")
            new_audio_data[sample_index] = (sample & 0xFFF8) | 0b111
            msg_index += 1
            space_found = True
        else:
            new_audio_data[sample_index] = sample & 0xFFF8

        sample_index += 1

    if msg_index == 0:
        print("[!] Can not hide any character. Not enough space.")
        return

    while sample_index < len(new_audio_data):
        new_audio_data[sample_index] &= 0xFFF8
        sample_index += 1

    if msg_index == total_chars:
        with wave.open(output_audio, 'wb') as out_audio:
            out_audio.setparams(params)
            out_audio.writeframes(new_audio_data.tobytes())
        print("✅ Successfully. Audio file was saved in", output_audio)
    else:
        print("[!] Not enough space to hide the message. ", msg_index, "were saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Giấu thông điệp vào file âm thanh.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', type=str, help="Đường dẫn tới file chứa thông điệp văn bản.")
    group.add_argument('-b', '--binary', type=str, help="Đường dẫn tới file chứa thông điệp dạng nhị phân.")
    parser.add_argument('-s', '--sound', type=str, required=True, help="Đường dẫn tới file âm thanh đầu vào (wav).")
    parser.add_argument('-o', '--output', type=str, default="output.wav", help="Tên file âm thanh đầu ra (mặc định: output.wav)")

    args = parser.parse_args()

    message_bytes = read_message_bytes(text_file=args.file, binary_file=args.binary)
    embed_message_in_audio(args.sound, args.output, message_bytes)


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

def make_lsb_odd(sample):
    """Chỉnh nhẹ nhất để 4 LSB có số bit 1 lẻ."""
    lsb = sample & 0xF
    if bin(lsb).count('1') % 2 == 0:  # Nếu số bit 1 hiện tại chẵn
        sample ^= 0x1  # Đảo bit thấp nhất
    return sample

def make_lsb_even(sample):
    """Chỉnh nhẹ nhất để 4 LSB có số bit 1 chẵn."""
    lsb = sample & 0xF
    if bin(lsb).count('1') % 2 == 1:  # Nếu số bit 1 hiện tại lẻ
        sample ^= 0x1
    return sample

def embed_message_in_audio(input_audio, output_audio, message_file):
    with open(message_file, 'r') as f:
        message = f.read().strip()

    print("Steganography is under processing ...")
    message_bytes = [ord(c) for c in message]
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
            print(f"[+] Found appropriate MSB: {sample_msb} (Character '{chr(current_char)}')")
            new_audio_data[sample_index] = make_lsb_odd(sample)
            msg_index += 1
            space_found = True
        else:
            new_audio_data[sample_index] = make_lsb_even(sample)

        sample_index += 1

    if msg_index == 0:
        print("[!] Can not hide any character. Not enough space.")
        return

    # Sau khi giấu xong, tiếp tục đảm bảo phần còn lại LSB là chẵn
    while sample_index < len(new_audio_data):
        new_audio_data[sample_index] = make_lsb_even(new_audio_data[sample_index])
        sample_index += 1

    if msg_index == total_chars:
        with wave.open(output_audio, 'wb') as out_audio:
            out_audio.setparams(params)
            out_audio.writeframes(new_audio_data.tobytes())
        print("✅ Successfully. Audio file was saved in ", output_audio)
    else:
        print("[!] Not enough space to hide the message. ", msg_index, " characters were saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Giấu thông điệp vào file âm thanh.")
    parser.add_argument('-f', '--file', type=str, required=True, help="Đường dẫn tới file thông điệp.")
    parser.add_argument('-s', '--sound', type=str, required=True, help="Đường dẫn tới file âm thanh đầu vào (wav).")
    parser.add_argument('-o', '--output', type=str, default="output.wav", help="Tên file âm thanh đầu ra (mặc định: output.wav)")

    args = parser.parse_args()
    embed_message_in_audio(args.sound, args.output, args.file)


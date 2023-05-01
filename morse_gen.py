import time
import argparse
import playsound
import struct
import math
from os import path

# Morse code dictionary
morse_dict = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
              'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
              'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
              'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
              '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--',
              '?': '..--..', '/': '-..-.', '@': '.--.-.', ' ': '/'}

SCALE = 10

# Generate the audio dot.wav and dash.wav
# dot.wav: 1kHz, 0.1s
def audio_dot():
    dot = []
    for i in range(0, SCALE * 4410):
        dot.append(int(round(32767 * math.sin(2 * math.pi * 1000 * i / 44100))))
    dot_path = path.join(path.dirname(__file__), 'dot.wav')
    with open(dot_path, 'wb') as f:
        f.write(b''.join(struct.pack('<h', x) for x in dot))

# dash.wav: 1kHz, 0.2s
def audio_dash():
    dash = []
    for i in range(0, SCALE * 8820):
        dash.append(int(round(32767 * math.sin(2 * math.pi * 1000 * i / 44100))))
    dash_path = path.join(path.dirname(__file__), 'dash.wav')
    with open(dash_path, 'wb') as f:
        f.write(b''.join(struct.pack('<h', x) for x in dash))


# silence.wav: 0.1s
def audio_silence():
    silence = []
    for i in range(0, SCALE * 4410):
        silence.append(0)
    silence_path = path.join(path.dirname(__file__), 'silence.wav')
    with open(silence_path, 'wb') as f:
        f.write(b''.join(struct.pack('<h', x) for x in silence))


def morse_encode(s):
    s = s.upper()
    encoded = []
    for char in s:
        if char in morse_dict:
            encoded.append(morse_dict[char])
    return ' '.join(encoded)


def play_morse_audio(morse_encoded):
    for char in morse_encoded:
        if char == '.':
            playsound.playsound('dot.wav')
            time.sleep(0.1)
        elif char == '-':
            playsound.playsound('dash.wav')
            time.sleep(0.2)
        elif char == ' ':
            time.sleep(0.2)
        elif char == '/':
            time.sleep(0.4)


def save_audio(morse_encoded, filename):
    audio = []
    for char in morse_encoded:
        if char == '.':
            audio.append('dot.wav')
            audio.append('silence.wav')
        elif char == '-':
            audio.append('dash.wav')
            audio.append('silence.wav')
        elif char == ' ':
            audio.append('silence.wav')
            audio.append('silence.wav')
        elif char == '/':
            audio.append('silence.wav')
            audio.append('silence.wav')
            audio.append('silence.wav')
    audio_path = path.join(path.dirname(__file__), filename)
    with open(audio_path, 'wb') as f:
        f.write(b''.join(open(filename, 'rb').read() for filename in audio))


def main():

    # Generate the audio files
    audio_dot()
    audio_dash()
    audio_silence()

    # Parse the input string
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_str', help='input string', required=True)
    parser.add_argument('-f', '--filename', help='filename', default='morse_code.wav')
    args = parser.parse_args()
    input_str = args.input_str
    filename = args.filename

    # Encode the input string
    morse_encoded = morse_encode(input_str)
    save_audio(morse_encoded, filename)
    play_morse_audio(morse_encoded)


if __name__ == '__main__':
    main()

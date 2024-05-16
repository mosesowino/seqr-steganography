import numpy as np
from pydub import AudioSegment
import io

def message_to_binary(message):
    """Converts string message to binary."""
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_message(binary):
    """Converts binary string back to string."""
    message = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return message

def encode_aud_data(audio_segment, message):
    """Encodes a message into an audio segment using LSB."""
    # Convert message to binary
    binary_message = message_to_binary(message + '####')  # Adding '####' as a delimiter
    samples = np.array(audio_segment.get_array_of_samples())

    if len(binary_message) > len(samples):
        raise ValueError("Message is too long to be encoded in the provided audio.")

    # Encode binary message into the least significant bit of each sample
    new_samples = samples.copy()
    for i, bit in enumerate(binary_message):
        new_samples[i] = (new_samples[i] & ~1) | int(bit)

    # Create a new audio segment with the modified samples
    encoded_audio = audio_segment._spawn(new_samples.tobytes())
    return encoded_audio

def decode_aud_data(encoded_audio_segment):
    """Decodes a message from an audio segment using LSB."""
    samples = np.array(encoded_audio_segment.get_array_of_samples())
    binary_message = ''.join(str(sample & 1) for sample in samples)  # Extract LSB from each sample

    # Extract message until the delimiter '####'
    try:
        delimiter = binary_message.index('00100011001000110010001100100011')  # Binary for '####'
        binary_message = binary_message[:delimiter]
        return binary_to_message(binary_message)
    except ValueError:
        raise ValueError("No message found or incorrect delimiter.")

# Example usage

audioPath = "C:/Users/user/Desktop/Steganography-Tools-master/Sample_cover_files/cover_audio.wav"
path_to_audio = audioPath

# audio = AudioSegment.from_file(path_to_audio, format='wav')
# encoded_audio = encode_aud_data(audio, "Hello World")
# encoded_audio.export("encoded_audio.wav", format="wav")
# decoded_message = decode_aud_data(AudioSegment.from_file('encoded_audio.wav', format='wav'))#call with the first argument as a path
# print("Decoded Message:", decoded_message)
import sys
import math
from os import path
import cv2
import numpy as np

BIT_DEPTH = 2

BIT_MASK_HIGH = 256 - (1 << BIT_DEPTH)
BIT_MASK_LOW = (1 << BIT_DEPTH) - 1
BYTES_PER_PIXEL = math.ceil(8 / BIT_DEPTH)
MESSAGE_DELIMITER = '%'
ENCODED_IMAGE_PATH = path.abspath("downloads/encoded_image.png")

def encode_image_data(image_path, message):
    def insert_message_into_image(image_path, message):
        print(f"Image path: {image_path}")
        print(f"Encoded image save path: {ENCODED_IMAGE_PATH}")
        image = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)
        max_bytes_capacity = image.shape[0] * image.shape[1] // BYTES_PER_PIXEL
        
        # Encode message with length
        message_with_length = f'{len(message)}{MESSAGE_DELIMITER}{message}'
        assert max_bytes_capacity >= len(message_with_length), "Message exceeds image capacity:{}".format(max_bytes_capacity)
        
        flat_image_data = np.reshape(image, -1)
        
        for index, character in enumerate(message_with_length):
            encode_character(flat_image_data[index * BYTES_PER_PIXEL: (index + 1) * BYTES_PER_PIXEL], character)

        reshaped_image = np.reshape(flat_image_data, image.shape)
        filename, _ = path.splitext(ENCODED_IMAGE_PATH)
        filename += '.png'
        cv2.imwrite(filename, reshaped_image)
        return filename


    def encode_character(image_block, character):
        char_code = ord(character)
        for index in range(len(image_block)):
            image_block[index] &= BIT_MASK_HIGH
            image_block[index] |= (char_code >> (BIT_DEPTH * index)) & BIT_MASK_LOW
            
    return insert_message_into_image(image_path, message)

def decode_image_data(image_path):
    def extract_message_from_image(image_path):
        image = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)
        flat_image_data = np.reshape(image, -1)
        total_bytes = flat_image_data.shape[0]
        extracted_message_length = ''
        byte_index = 0
        
        # Decode message length
        while byte_index < total_bytes // BYTES_PER_PIXEL:
            character = decode_character(flat_image_data[byte_index * BYTES_PER_PIXEL: (byte_index + 1) * BYTES_PER_PIXEL])
            byte_index += 1
            if character == MESSAGE_DELIMITER:
                break
            extracted_message_length += character
        
        message_length = int(extracted_message_length)
        end_index = message_length + byte_index
        assert end_index <= total_bytes // BYTES_PER_PIXEL, "Input image data is corrupted or incorrect."

        secret_message = ''
        while byte_index < end_index:
            secret_message += decode_character(flat_image_data[byte_index * BYTES_PER_PIXEL: (byte_index + 1) * BYTES_PER_PIXEL])
            byte_index += 1
        return secret_message


    def decode_character(image_block):
        char_code = 0
        for index in range(len(image_block)):
            char_code |= (image_block[index] & BIT_MASK_LOW) << (index * BIT_DEPTH)
        return chr(char_code)
    
    return extract_message_from_image(image_path)


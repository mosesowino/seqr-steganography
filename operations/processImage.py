import sys
import math
from os import path
import cv2
import numpy as np

# Embed secret in the n least significant bit.
# Lower n make picture less loss but lesser storage capacity.
BITS = 2

HIGH = 256 - (1 << BITS)
LOW = (1 << BITS) - 1
BYTES_PER_PIXEL = math.ceil(8 / BITS)
DELIMITER = '%'
DOWNLOAD_IMG_PATH = path.abspath("downloads/encoded_image.png")

def encode_img_data(img_path, msg):
    def insert(img_path, msg):
        print(f"img_path ---> {img_path}")
        print(f"\n download_path ---> {DOWNLOAD_IMG_PATH}")
        img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
        max_bytes = img.shape[0] * img.shape[1] // BYTES_PER_PIXEL
        
        # Encode message with length
        msg = '{}{}{}'.format(len(msg), DELIMITER, msg)
        assert max_bytes >= len(
            msg), "Message greater than capacity:{}".format(max_bytes)
        data = np.reshape(img, -1)
        
        for (idx, val) in enumerate(msg):
            encode(data[idx*BYTES_PER_PIXEL: (idx+1) * BYTES_PER_PIXEL], val)

        img = np.reshape(data, img.shape)
        filename, _ = path.splitext(DOWNLOAD_IMG_PATH)
        filename += '.png'
        img = cv2.imwrite(filename, img)
        return filename


    def encode(block, data):
        # returns the Unicode code from a given character
        data = ord(data)
        for idx in range(len(block)):
            block[idx] &= HIGH
            block[idx] |= (data >> (BITS * idx)) & LOW
            
            
    return insert(img_path, msg)




def decode_img_data(path):
    def extract(path):
        img = cv2.imread(path, cv2.IMREAD_ANYCOLOR)
        data = np.reshape(img, -1)
        total = data.shape[0]
        res = ''
        idx = 0
        # Decode message length
        while idx < total // BYTES_PER_PIXEL:
            ch = decode(data[idx*BYTES_PER_PIXEL: (idx+1)*BYTES_PER_PIXEL])
            idx += 1
            if ch == DELIMITER:
                break
            res += ch
        end = int(res) + idx
        assert end <= total // BYTES_PER_PIXEL, "Input image isn't correct."

        secret = ''
        while idx < end:
            secret += decode(data[idx*BYTES_PER_PIXEL: (idx+1)*BYTES_PER_PIXEL])
            idx += 1
            # print(secret)
        return secret


    def decode(block):
        val = 0
        for idx in range(len(block)):
            val |= (block[idx] & LOW) << (idx * BITS)
        return chr(val)
    
    return extract(path)



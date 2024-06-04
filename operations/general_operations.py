import numpy as np
from pydub import AudioSegment
from os import path


CURRENT_DIR = path.dirname(__file__)
UPLOADED_FILES_DIR = path.join(CURRENT_DIR, '..', 'uploaded_files')


def BinaryToDecimal(binary: str) -> str:
    decimal: str = int(binary, 2)
    return decimal




def MessageToBinary(message):
    if type(message) == str:
        result= ''.join([ format(ord(i), "08b") for i in message ])
    
    elif type(message) == bytes or type(message) == np.ndarray:
        result= [ format(i, "08b") for i in message ]
    
    elif type(message) == int or type(message) == np.uint8:
        result=format(message, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    
    print(result)
    return result


def determineFileType(filename) -> str:
    # Mapping from extension to file type
    extension_mapping = {
        '.jpg': 'image', '.jpeg': 'image', '.png': 'image',
        '.mp3': 'audio', '.wav': 'audio'
    }
    
    # Extract the file extension and convert to lowercase
    extension = filename.rsplit('.', 1)[-1].lower()
    if '.' + extension in extension_mapping:
        return extension_mapping['.' + extension]
    else:
        return "unknown"


def determineMediaType(filename) -> str:
    return filename.rsplit('.', 1)[-1].lower()
   


def Mp3ToWav(filepath) -> object:
    sound = AudioSegment.from_mp3(filepath)
    # file = 'encoded_mp3.mp3'
    # converted_to_mp3_filepath = path.join(UPLOADED_FILES_DIR, file)
    # sound.export(converted_to_mp3_filepath,format='wav') 
    # return converted_to_mp3_filepath
    return sound
    
def WavToMp3(filepath) -> object:
    sound = AudioSegment.from_wav(filepath)
    # sound.export(mp3_file, format='mp3', bitrate=bitrate)
    return sound
    
    
# current_dir = path.dirname(__file__)   
# target_file = path.abspath(path.join(current_dir, '..', 'uploaded_files','audio.mp3'))
# # abs_path = path.abspath("./uploaded_files/audio_on_what_quantitative_skills_entail.mp3")


# aud_path = "C:/Users/user/Desktop/tchzn/python/final_project/uploaded_files/audio.mp3"
# print(f"path of converted audio is --> {Mp3ToWav(aud_path)}")

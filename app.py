from flask import Flask, send_file, request, redirect, url_for, jsonify
from flask import render_template
from PIL import Image
from pydub import AudioSegment
import io
import numpy as np
import cv2
import wave
import os
from operations import general_operations, processImage, processAudio
from werkzeug.utils import secure_filename, redirect
from flask_cors import CORS, cross_origin
import mysql.connector

app = Flask(__name__)


CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'seqr'

EXAMPLE_SQL = 'select * from seqr.users where email = %s and username = %s'
LOGIN ="select * from seqr.users where username = %s and password = %s"
REGISTER = "INSERT INTO users VALUES(%s,%s,%s)"
LOGGED_IN = False
USERNAME = ''
PASSWORD = ''
EMAIL = ''

def get_db_connection():
    return mysql.connector.connect(
        host = app.config['MYSQL_HOST'],
        user = app.config['MYSQL_USER'],
        database = app.config['MYSQL_DATABASE']
    )

@app.route('/data')
def get_data():
    email = ('user1@gmail.com')
    username = ('user1')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(EXAMPLE_SQL,(email,username))
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

@app.route('/', methods=['POST', 'GET'])
def index():
    CONN = get_db_connection()
    CURSOR = CONN.cursor(dictionary=True)
    global USERNAME, PASSWORD, EMAIL
    
    if request.method == "GET":
        return render_template('index.html')
    
    if request.method == "POST":
        if len(request.form) == 2:
            USERNAME = request.form.get("username")
            PASSWORD = request.form.get("password")
            EMAIL = False
            
        elif len(request.form) == 3:
            USERNAME = request.form.get("username")
            EMAIL = request.form.get("email")
            PASSWORD = request.form.get("password")
            print(f"Email------>{EMAIL}")
            print(f"Password ------>{PASSWORD}")
        
        if not EMAIL:
            CURSOR.execute(LOGIN,(USERNAME, PASSWORD))
            rows = CURSOR.fetchone()
            CURSOR.close()
            if not rows:
                return "Invalid credentials, try Again"
            
            global LOGGED_IN
            LOGGED_IN = True
            # return f"Active: {LOGGED_IN}"
            if LOGGED_IN:
                return redirect('/main')
        
        elif EMAIL:
            try:
                CURSOR.execute(REGISTER,(USERNAME,EMAIL,PASSWORD))
                CONN.commit()
                CURSOR.close()
                return redirect('/main')
            except:
                return 'Registration failed'
                
            
            

        
def file_typeSpecificEncoding (file_type: str, message, filename):
    match file_type:
        case "audio":
            return encode_audio(message, filename)
        case "image":
            return encode_image(message, filename)
        case "video":
            return encode_video(message, filename)
        case _:
            return "Unsupported file type"

def file_typeSpecificDecoding(file_type, filename):
        match file_type:
            case "audio":
                return decode_audio(filename)
            case "image":
                return decode_image(filename)
            case "video":
                return decode_video(filename)
            case _:
                return "Unsupported file type"
                
        
@app.route('/main', methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        return render_template('main.html',username=USERNAME, active=LOGGED_IN)
        
    elif request.method == "POST":
        # data = request.form.get("secret_message")
        FILE_KEY = "file_to_encode"
        try:
            secret_message = request.form["secret_message"]
        except:
            encode = False
            FILE_KEY = "file_to_decode"
        else:
            encode = True
            
        file = request.files[FILE_KEY]
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploaded_files', filename)
        # file.save('uploaded_files/' + file.filename)
        file.save(filepath)
        
        
        file_type: str = general_operations.determineFileType(filename)
        
        if encode:
            encoding_response =  file_typeSpecificEncoding(file_type, secret_message, filepath)
            if isinstance(encoding_response, str):
                if encoding_response.startswith("Unsupported"):
                    return encoding_response
                else:
                    return send_file(encoding_response, as_attachment=True)
            else:

                return "An error occurred, please try again."
            
            
        else:
            try:
                decoding_response =  file_typeSpecificDecoding(file_type, filepath)
            except ValueError:
                decoding_response = "No Message Found !"
           
            global msg 
            msg = decoding_response
            
            return render_template('main.html',message=msg,username=USERNAME, active=LOGGED_IN)
            
    else:
        return redirect(url_for('home')) 



@app.route('/about', methods=['POST','GET'])
def about():
    return render_template('about.html')

def encode_image(message, filename):

    encoded_img = processImage.encode_image_data(filename, message)

    
    return os.path.abspath(encoded_img)
    
    
    
def decode_image(filename):
    decoded_message = processImage.decode_image_data(filename)
    
    return decoded_message



def encode_audio(message, filepath):
   
    audio = AudioSegment.from_file(filepath, format='wav')
    encoded_audio_file = processAudio.encode_aud_data(audio, message)
    

    output_path = 'downloads/encoded_audio.wav'
    
    encoded_audio_file.export(output_path, format="wav")
    
    # if was_mp3:
    #     sound = general_operations.WavToMp3(output_path)

    return output_path



def decode_audio(filepath):
    file = AudioSegment.from_file(filepath, format='wav')
    decoded_message = processAudio.decode_aud_data(file)
    return decoded_message


# def Mp3ToWav(filepath) -> object:
#     sound = AudioSegment.from_mp3(filepath)
#     # file = 'encoded_mp3.mp3'
#     # converted_to_mp3_filepath = path.join(UPLOADED_FILES_DIR, file)
#     sound.export(converted_to_mp3_filepath,format='wav') 
#     # return converted_to_mp3_filepath
#     # return sound




if __name__ == '__main__':
    app.run(debug=True)
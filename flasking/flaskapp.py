import os
from PIL import Image
import soundfile as sf
from pydub import AudioSegment
import numpy as np
import cv2
import ffmpeg
import uuid
import base64
from ipywidgets import FileUpload
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask import *

app = Flask(__name__, static_url_path='')

def compressPNG(origfile, newfile):
    img=Image.open(origfile)
    img=img.convert("P", palette=Image.ADAPTIVE, colors=256)
    img.save(newfile, optimize=True)

def compressJPEG(origfile,newfile):
    img=Image.open(origfile)
    if img.mode == "JPEG":
        img.save(newfile)
    else:
        rgb_im = img.convert("RGB")
        rgb_im.save(newfile)

def compressVid(origfile,newfile):
    os.system(f'ffmpeg -i {origfile} -vf "scale=trunc(iw/4)*2:trunc(ih/4)*2" -c:v libx265 -crf 28 {newfile}')


def compressWAV(origfile, newfile):
    data, samplerate=sf.read(origfile)
    n=len(data)
    Fs=samplerate
    ch1=np.array([data[i][0] for i in range(n)])
    ch2=np.array([data[i][1] for i in range(n)])
    ch1_Fourier=np.fft.fft(ch1)
    abs_ch1_Fourier=np.absolute(ch1_Fourier[:n//2])
    eps=1e-5
    frequenciesToRemove = (1-eps) * np.sum(abs_ch1_Fourier) < np.cumsum(abs_ch1_Fourier)
    f0=(len(frequenciesToRemove)- np.sum(frequenciesToRemove))*(Fs/2)/(n/2)
    D=int(Fs/f0)
    new_data=data[::D,:]
    sf.write(newfile, new_data, int(Fs/D), 'PCM_16')

def compressMP3(origfile, newfile):
    tempname1=str(uuid.uuid4())+".wav"
    tempname2=str(uuid.uuid4())+".wav"
    audio=AudioSegment.from_mp3(origfile)
    audio.export(tempname1, format="wav")
    compressWAV(tempname1, tempname2)
    audio2=AudioSegment.from_wav(tempname2)
    audio2.export(newfile, format="mp3")
    os.remove(tempname1)
    os.remove(tempname2)

def compressOthers(origfile,newfile): #No compression
    f1=open(origfile,'rb').read()
    f2=open(newfile,'wb')
    f2.write(f1)
    f2.close()

def setBitrate():
    os.environ['BITRATE']='16'
    #Bitrate 16 uses 4 channels, namely 2000Hz, 3000Hz, 4000Hz, 5000Hz

def file_compress(fln):
    ext=os.path.splitext(fln)[1]
    newname=str(uuid.uuid4())+ext
    if ext=='.png' or ext == '.PNG':
        compressPNG(fln, newname)
    elif ext=='.jpg' or ext=='.JPG' or ext=='.JPEG' or ext=='.jpeg':
        compressJPEG(fln,newname)
    elif ext=='.mp4' or ext=='.MP4':
        compressVid(fln, newname)
    elif ext=='.wav' or ext=='.WAV':
        compressWAV(fln, newname)
    elif ext=='.mp3' or ext=='.MP3':
        compressMP3(fln,newname)
    else:
        compressOthers(fln,newname)
    file = open(newname, 'rb')
    file_content = file.read()
    file.close()
    os.remove(newname)
    return file_content

def no_compress(fln):
    file = open(fln, 'rb')
    file_content = file.read()
    file.close()
    return file_content

def genCryptoKey(psk):
    salt=b'\xab\xa6\xbfx\xf1s \xf7R\x88DU$\xb3\x021'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=390000,)
    key = base64.urlsafe_b64encode(kdf.derive(psk.encode()))
    f = Fernet(key)
    print(key)
    return f

def encrypt(data, psk):
    fkey = genCryptoKey(psk)
    encdata=fkey.encrypt(data)
    return encdata

def decrypt(encdata, psk):
    fkey = genCryptoKey(psk)
    data=fkey.decrypt(encdata)
    return data

def save_temp(tempdata):
    tempname=str(uuid.uuid4())
    with open(tempname, 'wb') as f:
        f.write(tempdata)
    os.environ['tempname']=tempname
    return tempname

def send_data(tempname):
    os.system("amodem send -vv -i "+tempname)

def recv_data(tempname):
    os.system("amodem recv -vv -o "+tempname)

def cleanup():
    global fln
    os.remove(fln)
    os.remove(tempname)

@app.route("/send_page", methods=["GET", "POST"])
def send_page():
    return render_template("send.html")

@app.route("/send", methods=["GET","POST"])
def send():
    print(request.form.getlist('check'))
    fln=request.files['file'].filename
    print(fln)
    f=request.files['file']
    f.save(f.filename)
    if 'encrypt' in request.form.getlist('check'):
        encryption=True
        psk=request.form['psk']
    else:
        encryption=False
    if 'compress' in request.form.getlist('check'):
        compress=True
    else:
        compress=False

    if compress:
         file_content=file_compress(fln)
    else:
         file_content=no_compress(fln)

    flnlen=len(fln).to_bytes(1,byteorder='big')
    metadata=flnlen+fln.encode()
    data=metadata+file_content
    
    if encryption:
        tempdata=encrypt(data, psk)
    else:
        tempdata=data
    tempname=save_temp(tempdata)
    tempsize = os.path.getsize(tempname)
    print(f"Attempting to send {tempsize} bytes")
    print("Make sure receiver is listening")
    send_data(tempname)
    return "Sent"

@app.route("/recv_page", methods=["GET","POST"])
def recv_page():
    return render_template("receive.html")

@app.route("/recv", methods=["GET", "POST"])
def recv():
    if 'encrypt' in request.form.getlist('check'):
        encryption=True
        psk=request.form['psk']
    else:
        encryption=False
    tempname=str(uuid.uuid4())
    os.environ['tempname']=tempname
    recv_data(tempname)
    with open(tempname,'rb') as f:
        tempdata=f.read()
    if encryption:
        data=decrypt(tempdata, psk)
    else:
        data=tempdata
    flnlen=data[0]
    fln=data[1:(flnlen+1)].decode()
    file_content=data[(flnlen+1):]
    file=open(fln,'wb')
    file.write(file_content)
    file.close()
    return send_from_directory(directory='.', path=fln)

if __name__=='__main__':
    app.run(port=5000)

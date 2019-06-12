#!/usr/bin/env python

from flask import Flask
import requests
import io
import base64
import json
import glob, os
from os.path import basename
import picamera
result = True

app = Flask(__name__)

@app.route('/result')
def resultHandler():
    global result
    if result == True:
        result = False;
        return 'True'
    else:
        return 'False'

@app.route('/hello')
def helloWorldHandler():
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture("/home/pi/315/newimage.jpg")

    print ("picture taken")


    # put your keys in the header
    headers = {
        "app_id": "c368ba7a",
        "app_key": "ed6d001d8283bca7b85419d8e520619d"
    }

    img_path = "newimage.jpg"
    dir_path = '/home/pi/315/'

    #os.chdir(dir_path)
    files = {'image': (img_path, open(dir_path + img_path, 'rb'), 'image/jpg', {'Expires': '0'})}

    values_enroll = {
           'gallery_name':'MyGallary0'
        }

    url = "http://api.kairos.com/recognize"

    # make request
    r = requests.post(url, headers = headers, files=files, data=values_enroll)
    print (r.content)

    # write image JSON respond to image_info.txt
    str = r.text
    image_info = open("image_info.txt", "w+")
    image_info.write(str)
    image_info.close()

    # processing image_info.txt to retrieve subject_id

    # This line is hard coded, will connect to MangoDB later
    global result
    subject_id1 = "Xiao"
    subject_id2 = "XinHe"
    subject_id3 = "Professor"
    if subject_id1 in open("image_info.txt").read():
        result = True;
        return 'True'
    if subject_id2 in open("image_info.txt").read():
        result = True
        return 'True'
    if subject_id3 in open("image_info.txt").read():
        result = True
        return 'True'
    
    result = False;
    return 'False'

app.run(host='0.0.0.0', port = 8090)

#!/usr/bin/python
 
import RPi.GPIO as GPIO
import time
import picamera
import datetime
import subprocess
import dropbox
import os
import smtplib

#send mail
def mailsend():
#Enter receiver email address
    toaddr = "receiver email"
#Enter sender email address
    fromaddr = "sender gmail"
#Enter sending message
    msg = 'Enter message'
#Enter your password
	password = "enter sender password"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "password")
    server.sendmail(fromaddr, toaddr, msg)
    print 'Message Sent!'
    server.quit()
 
#function for generating recording file name
def getFileName():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
def dropboxUpload(fileToUpload):
    # make client
    client = dropbox.client.DropboxClient('Enter your dropbox access token')
 
    #upload file
    fileToUploadObject = open(fileToUpload, 'rb')
    response = client.put_file(fileToUpload, fileToUploadObject)
    fileToUploadObject.close()
 
sensorPin = 7
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
prevState = False
currState = False
 
cam = picamera.PiCamera()
 
while True:
    time.sleep(0.1)
    prevState = currState
    currState = GPIO.input(sensorPin)
    if currState != prevState:
        newState = "HIGH" if currState else "LOW"
        print "GPIO pin %s is %s" % (sensorPin, newState)
        if currState:
            fileName = getFileName()
            print "Starting Recording..."
            cam.start_preview()
            cam.start_recording(fileName)
            print (fileName)
        else:
            cam.stop_preview()
            cam.stop_recording()
            print "Stopped Recording"
            print "Sending Mail Notification..."
            mailsend()
            print "Complete"
            print "Uploading footage to Dropbox..."
            dropboxUpload(fileName)
            print "Complete"
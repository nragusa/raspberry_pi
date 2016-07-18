#!/usr/bin/env python

from picamera import PiCamera
from time import time, sleep
import boto3

"""CONFIG"""
WARM_UP = 3 # Seconds to wait for camera to warm up 
FREQUENCY = 5 # Seconds between stills are taken
LOCAL_PATH = '/dev/shm'
S3_BUCKET = 'your-s3-bucket'
S3_PREFIX = 'images/'

"""Initialize s3 client and camera"""
s3_client = boto3.client('s3')
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

print('Waiting {} seconds to warm up...'.format(WARM_UP))
sleep(WARM_UP)

while True:
    """Take a picture and save locally"""
    filename = '{}/{}.jpg'.format(LOCAL_PATH, time())
    camera.capture(filename)

    """Upload image to S3"""
    with open(filename, 'rb') as f:
        key = '{}/{}'.format(S3_PREFIX,filename)
        response = s3_client.put_object(Body=f,Bucket=S3_BUCKET,Key=key)

    print('Response code: {}'.format(response['ResponseMetadata']['HTTPStatusCode']))
    sleep(FREQUENCY)
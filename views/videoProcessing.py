#-*- coding: utf-8 -*-
# 한글 사용을 위한 comment

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import urllib
from django.views.generic import View
import os
import requests


# AWS Python SDK
import boto3
from botocore.client import Config

# For OpenCV
import cv2
import numpy as np

# Internal Dependency
from openCV import processing
from mergeTimeAt import mergeTimeAt

s3 = boto3.resource('s3', 'ap-northeast-2')

LOCAL_MODE = "http://localhost:3000"
REMOTE_MODE = "http://ec2-52-79-77-112.ap-northeast-2.compute.amazonaws.com"

# Todo: Need to Set LOCAL_MODE or REMOTE_MODE
MODE = REMOTE_MODE

NODE_API = LOCAL_MODE if MODE == LOCAL_MODE else REMOTE_MODE

class videoProcessing(View):
    def get(self, request, *args, **kwargs):
        # Print out bucket names
        for bucket in s3.buckets.all():
            print(bucket.name)
        return JsonResponse({'message': 'This is GET Request'})


    '''
    post.body data is
    {
        "s3Url" : "hi",
        "email": "1",
        "ballColor": "#FFFFFF"
    }
    '''

    # Todo List
    # (V) 1. S3 에서 다운받음. (URl 로부터 비디오 스트림을 받을 수 있나?) => 그냥 다운받고 프로세싱하자. cpu 무리갈듯. Task Queue 이용할까, cron?
    # (V) 2. 이미지 프로세싱.
    # (V) 3. Video Write
    # (V) 4. S3 에 업로드
    # (V) 5. 파일 삭제
    # (V) 6. Node 서버에게 영상작업 완료되었다고 전달.
    # 7. Node 서버는 처리 완료된 S3 링크를 유져에게 전달.
    # AVC1 => mov 는 잘 동작.

    def post(self, request, *args, **kwargs):
        jsonBody = json.loads(request.body)
        s3Url = jsonBody['s3Url']
        email = jsonBody['email']
        ballColor = jsonBody['ballColor']
        token = jsonBody['token']
        fileNameWithExtension = s3Url.split('/')[-1]
        onlyFileName = fileNameWithExtension.split('.')[0]
        # FFMPEG backend with MP4 container natively uses other values as fourcc code:
        # see ObjectType, so you may receive a warning message from OpenCV about fourcc code conversion.
        outputFileName = onlyFileName + '-output.mp4'
        # 선 응답 후 처리? http://docs.celeryproject.org/

        if token != 'dfisdfn2@#23sdfbjsdfj23klnSDFn1l32nlkndskdskfjs@#f@!#dsf':
            return JsonResponse({'isSuccess': False, 'message': 'Token is Invalid'})

        # File Download from url
        print 'Download Start'
        urllib.urlretrieve(s3Url, fileNameWithExtension)
        print 'Download Success'

        # Image Processing
        ########################################################
        ################## Todo: CV Logic Start ################
        ########################################################
        timeArr = processing(fileNameWithExtension) # 받아온 파일을 openCV Processing
        ########################################################
        ################## Todo: CV Logic End ################
        ########################################################

        # S3에 업로드
        # Todo: 업로드후, 클라이언트로 요청해야만 받을 수 있나?
        # data = open(outputFileName, 'rb')
        data = open(fileNameWithExtension, 'rb')
        client = boto3.client('s3', config=Config(signature_version='s3v4'))
        bucket_name = 'futsal-manager'

        resp = client.put_object(
            Bucket=bucket_name,
            Key=outputFileName,
            Body=data
        )
        print 'file upload success'

        print(resp)
        url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': outputFileName, })
        print('get s3 url ' + url)

        # S3에 업로드 후 삭제
        os.remove(fileNameWithExtension)  # remove original file

        # Todo: 하드코딩되어 있는 토큰을 설정에서 set하기

        payload = {'email': email, 'processedS3Url': url, 'token': 'dfisdfn2@#23sdfbjsdfj23klnSDFn1l32nlkndskdskfjs@#f@!#dsf', 'timeArr': mergeTimeAt(timeArr), 'fileName': onlyFileName + "-output"}
        postRequest = requests.post(NODE_API + '/highlight/edit', json=payload)
        print('Post request to node', postRequest)

        return JsonResponse({'isSuccess': True, 'message': 'This is POST Request', 'gotData': jsonBody, 'processedS3Url': s3Url})

    def file(selfself, request, *args, **kwargs):
        return JsonResponse({'message': 'This is File Request'})

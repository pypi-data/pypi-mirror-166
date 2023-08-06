#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:45:10 2021

@author: ross
"""
#https://github.com/aws-samples/amazon-textract-code-samples/blob/master/python/12-pdf-text.py

import boto3
import time
import json
#import ocrp
#from ocrp.aws.config import aws_config

aws_config =  {
    'region':'ap-southeast-2',
    'access_key':'',
    'secret_key':''
}

def startJob(s3BucketName, objectName, extraction_type='detect'):
    #response = None
    if extraction_type=='analysis':
        jobId = startAnalysisJob(s3BucketName, objectName)
        
    else:
        jobId = startDetectionJob(s3BucketName, objectName)
    
    return jobId

def startDetectionJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract' , 
                      aws_access_key_id = aws_config['access_key'], 
                      aws_secret_access_key = aws_config['secret_key'],
                      region_name = aws_config['region'],
                          verify = False)
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
            'Bucket': s3BucketName,
            'Name': objectName
            }
        })
    return response["JobId"]

def startAnalysisJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract' , 
                      aws_access_key_id = aws_config['access_key'], 
                      aws_secret_access_key = aws_config['secret_key'],
                      region_name = aws_config['region'],
                          verify = False)
    response = client.start_document_analysis(
        DocumentLocation={
            'S3Object': {
            'Bucket': s3BucketName,
            'Name': objectName
            }
        },
        FeatureTypes = ['TABLES','FORMS']
    )
    return response["JobId"]


def isJobComplete(jobId, extraction_type='detect'):
    # For production use cases, use SNS based notification 
    # Details at: https://docs.aws.amazon.com/textract/latest/dg/api-async.html
    if extraction_type=='analysis':
        status = isAnalysisJobComplete(jobId)
        
    else:
        status = isDetectionJobComplete(jobId)
        
    return status


def isDetectionJobComplete(jobId):
    # For production use cases, use SNS based notification 
    # Details at: https://docs.aws.amazon.com/textract/latest/dg/api-async.html
    time.sleep(5)
    client = boto3.client('textract' , 
                      aws_access_key_id = aws_config['access_key'], 
                      aws_secret_access_key = aws_config['secret_key'],
                      region_name = aws_config['region'],
                          verify = False)
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))
    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))
    return status

def isAnalysisJobComplete(jobId):
    # For production use cases, use SNS based notification 
    # Details at: https://docs.aws.amazon.com/textract/latest/dg/api-async.html
    time.sleep(5)
    client = boto3.client('textract' , 
                      aws_access_key_id = aws_config['access_key'], 
                      aws_secret_access_key = aws_config['secret_key'],
                      region_name = aws_config['region'],
                          verify = False)
    response = client.get_document_analysis(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))
    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_analysis(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))
    return status


def getJobResults(jobId, extraction_type='detect'):
    
    if extraction_type=='analysis':
        response = getAnalysisJobResults(jobId)
        
    else:
        response = getDetectionJobResults(jobId)
    
    return response
      
def getDetectionJobResults(jobId):
    
    client = boto3.client('textract' , 
                      aws_access_key_id = aws_config['access_key'], 
                      aws_secret_access_key = aws_config['secret_key'],
                      region_name = aws_config['region'],
                          verify = False)
    mega_response = client.get_document_text_detection(
            JobId=jobId
        )
    
    nextToken = None
    if('NextToken' in mega_response):
        nextToken = mega_response['NextToken']
    while(nextToken):
        response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)
        mega_response['Blocks'].extend(response['Blocks'])
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']
    #doc = trp.Document(mega_response)
    return mega_response

def getAnalysisJobResults(jobId):

    client = boto3.client('textract' , 
                      aws_access_key_id = aws_config['access_key'], 
                      aws_secret_access_key = aws_config['secret_key'],
                      region_name = aws_config['region'],
                          verify = False)
    mega_response = client.get_document_analysis(
            JobId=jobId
        )
    
    nextToken = None
    if('NextToken' in mega_response):
        nextToken = mega_response['NextToken']
    while(nextToken):
        response = client.get_document_analysis(JobId=jobId, NextToken=nextToken)
        mega_response['Blocks'].extend(response['Blocks'])
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']
    #doc = trp.Document(mega_response)
    return mega_response
    
# def getLogStream(log_group, limit_results=5):
    
#     client = boto3.client('logs', config=my_config)
#     parameters = {
#         "logGroupName": log_group,
#         "orderBy": "LastEventTime",
#         "desending":True
#         }
    
#     response = client.describe_log_streams(
#         **parameters)['logStreams'][:limit_results]
    
#     return response

# def getJsons(logs_dict, out_dir):
    
#     json_files = log_dict['DocumentName'].strip("")
    
#     out_bucket = ""
    
#     message
    
def upload_s3(file, s3_bucket, object_name):
    client = boto3.client('s3', 
                      aws_access_key_id = aws_config['access_key'], 
                      aws_secret_access_key = aws_config['secret_key'],
                      region_name = aws_config['region'],
                            verify = False)
    
    # s3_bucket = bucket + '/' + s3_folder
    # #object_name = s3_folder +'/'+ file.split('/')[-1]
    # object_name = file.split('/')[-1]
    response = client.upload_file(Filename=file, Bucket=s3_bucket, Key=object_name)
    print('file uploading {0}'.format(response))
    return response
    
    
def write_to_file(response, fname):
    
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)
        print('file written', fname)
          

# def push_to_bucket(inbucket, folder, pdf):
    
#     import subprocess
#     cmd = 'aws s3 cp '+pdf+' s3://'+inbucket+folder+ ' --sse AES256'
#     print(cmd)
    
#     push = subprocess.run(cmd, shell=True, stdout = subprocess.PIPE)
#     print(push.returncode)    
    
    
def batch_extract_files(fname, extraction_type='detect'):

    import os
    
    #import subprocess
    fname = ""
    data = '/Users/ross/GitHub/src/OCR/Textract/data/'
    #output = '/Users/ross/Pictures/bendigo/images/temp/'
    for top, dirs, files in os.walk(data):
        for filename in files:
            if filename.endswith('.png'):
                print(filename)
                #download
                s3BucketName = "handwriting-ocr"
                path = 'textract/images/'
                file_n = filename
                jobId = startJob(s3BucketName, path+file_n, extraction_type=extraction_type)
                print("Started job with id: {}".format(jobId))
                status = isJobComplete(jobId, extraction_type=extraction_type)
                
                if status =='SUCCEEDED':
                    response = getJobResults(jobId, extraction_type=extraction_type)
        
                    path = data
                    fname = path + file_n[:-3] + 'json'
                    write_to_file(response, fname)

    return fname


def textract(bucket, objectName, extraction_type='analysis'): 
    #objectName = pdf.split('/')[-1]
    jobId = startJob(bucket, objectName, extraction_type=extraction_type)
    print("Started job with id: {}".format(jobId))

    status = isJobComplete(jobId, extraction_type=extraction_type)
    
    if status =='SUCCEEDED':
        response = getJobResults(jobId, extraction_type=extraction_type)
        fname = pdf[:-3] + 'json'
        write_to_file(response, fname)

            
    return fname
    
if __name__ == "__main__":
    
    #s3 = session.resource('s3')
    bucket = "handwriting-ocr"
    


    

    
 
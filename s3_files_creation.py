import uuid
import json
import boto3
import multiprocessing
import json
from multiprocessing import Process

s3 = boto3.client('s3')

def create_test_files(bucket, file_path, no_of_files):
    print("bucket =", bucket)
    print("file_path =", file_path)
    print("no_of_files =", no_of_files)
    
    transactionToUpload = {}
    transactionToUpload['transactionId'] = '12345'
    transactionToUpload['type'] = 'PURCHASE PURCHASE PURCHASE PUR'
    transactionToUpload['amount'] = 20
    transactionToUpload['customerId'] = 'CID-11111'
    
    for lp in range(no_of_files):
        fileName = file_path + str(uuid.uuid4()) + '.json'
        uploadByteStream = bytes(json.dumps(transactionToUpload).encode('UTF-8'))
        s3.put_object(Bucket=bucket, Key=fileName, Body=uploadByteStream)
    

def lambda_handler(event, context):
    print(event)
    bucket = event['bucket_name']
    bucket_paths = json.loads(event['bucket_paths'].replace('\'', '"'))
    no_of_files = int(event['no_of_files'])
    print("bucket =", bucket)
    print("file_path =", bucket_paths)
    print("no_of_files =", no_of_files)
    procs = []

    for path in bucket_paths:
        print('creating a process for prefix = ', path)
        proc = Process(target=create_test_files, args=(bucket, path, no_of_files ))
        procs.append(proc)
        proc.start()

    # complete the processes
    for proc in procs:
        proc.join()
        

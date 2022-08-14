import json
import boto3
import multiprocessing
import json
from multiprocessing import Process
import time

s3_client = boto3.client('s3', region_name='eu-west-1')

def empty_the_s3_path(bucket, prefix):    
    time_to_sleep = 0    
    print('bucket_name = ',bucket, 'prefix = ', prefix)
    object_response_paginator = s3_client.get_paginator('list_object_versions')
    operation_parameters = {'Bucket': bucket, 'Prefix': prefix}
    delete_version_list = []    
    page_read_count = 0
    
    for object_response_itr in object_response_paginator.paginate(**operation_parameters):
        page_read_count = page_read_count + 1
        print("page_read_count = ", page_read_count)
        #print('object_response_itr = ', object_response_itr)
        if 'DeleteMarkers' in object_response_itr:
            for delete_marker in object_response_itr['DeleteMarkers']:
                delete_version_list.append({'Key': delete_marker['Key'], 'VersionId': delete_marker['VersionId']})
                #print('delete_marker[Key] = ', delete_marker['Key'])

        if 'Versions' in object_response_itr:
            for version in object_response_itr['Versions']:
                delete_version_list.append({'Key': version['Key'], 'VersionId': version['VersionId']})
                #print('version[Key] = ', version['Key'])
        try:            
            response = s3_client.delete_objects(
            Bucket=bucket,
            Delete={
                'Objects': delete_version_list,
                'Quiet': True}
            )            
            #print(response)
            #print('{0}/{1} Delete HTTPStatusCode={2}'.format(bucket, prefix, response['ResponseMetadata']['HTTPStatusCode']))
            """ Enalbe sleep when required. Please refer the documentation for further information on this"""
            #time.sleep(0.3)
        except Exception as ex:
            print("An exception occurred"+ str(ex))    
            time_to_sleep =  time_to_sleep +  exp_inc_step
            print("time_to_sleep = ", time_to_sleep)
            time.sleep(time_to_sleep)
            pass
        
        delete_version_list = []
        #print('len(delete_version_list) = ', len(delete_version_list))

def lambda_handler(event, context):
    #print('multiprocessing.cpu_count() =', multiprocessing.cpu_count())    
    print('event = ', event)
    print('bucket_name = ', event['bucket_name'])
    print('prefix_list = ', event['prefix_list'])
    bucket = event['bucket_name']
    prefix_list = json.loads(event['prefix_list'].replace('\'', '"'))
    procs = []
    
    # instantiating process with arguments
    for prefix in prefix_list:
        print('creating a process for prefix = ', prefix)
        proc = Process(target=empty_the_s3_path, args=(bucket, prefix))
        procs.append(proc)
        proc.start()

    # complete the processes
    for proc in procs:
        proc.join()
    



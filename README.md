# Context
Deletion or empty of versioning enalbed AWS S3 bucket is tedious. There is no simple option to do in single go especially if the bucket contains millions of files.
In this project a programatic approach is employed to do this job and we try to reach the maximum limits offered by the S3 to delete objects at full throttle.

S3 allows up to 3500 write requests on each prefix in the S3 buckets with DELETE API

The solution will use Lambda for the computing and EventBridge(EB) rules for the scheduling.

The complete solution looks as below:
Create a Lambda service role that has read and delete permission on the respective S3 bucket.

2. Write a Lambda function(GitHub link) with the following features:
It takes bucket_name and prefixes_list as input
Each prefix will create a sub-process
Using the boto3 S3 client and using pagination, get 1000 object versions in a single GET request
Using batch delete API, delete 1000 at a time
and repeat it till the objects in the prefix are empty

3. Create and schedule the EB rule to call the above Lambda three times in the same rule with input as bucket_name and prefixes_list for every 15/16 minutes.

# How to run?
Create a Lambda function with the code in the file "lambda_function.py"

This function would take two parameters: bucket_name, prefix_list

Example : 
```
{'bucket_name': 'fill-in-the-bucket-name', 'prefix_list': "['prefix/1/1','prefix/2/2']"}
```

Detailed explantion can found in this [blog post](https://medium.com/@rapurukirity/deletion-of-millions-of-objects-from-versioning-enabled-aws-s3-822461437d41)

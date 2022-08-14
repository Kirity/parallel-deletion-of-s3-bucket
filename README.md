# Context
Deletion or empty of versioning enalbed AWS S3 bucket is tedious. There is no simple option to do in single go especially if the bucket contains millions of files.
In this project a programatic approach is employed to do this job.

# How to run?
Create a Lambda function with the code in the file "lambda_function.py"

This function would take two parameters: bucket_name, prefix_list

Example : 
```
{'bucket_name': 'fill-in-the-bucket-name', 'prefix_list': "['prefix/1/1','prefix/2/2']"}
```

Detailed explantion can found in this [blog post](https://medium.com/@rapurukirity/deletion-of-millions-of-objects-from-versioning-enabled-aws-s3-822461437d41)

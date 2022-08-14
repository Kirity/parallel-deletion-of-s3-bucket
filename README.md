# Context
Deletion or empty of versioning enalbed AWS S3 bucket is a tedious job. 
There is no simple option to do in a single go especially if the bucket contains millions of files.
In this project a programatic approach is employed to do this job and we try to reach the maximum limits offered by the S3 to delete objects at full throttle.

# Solution

S3 allows up to 3500 write requests on each prefix in the S3 buckets with DELETE API.

The solution will use Lambda for the computing and EventBridge(EB) rules for the scheduling.

The complete solution looks as below:

1. Create a Lambda service role that has read and delete permission on the respective S3 bucket.

2. Write a Lambda function(GitHub link) with the following features:
- It takes bucket_name and prefixes_list as input
- Each prefix will create a sub-process
- Using the boto3 S3 client and using pagination, get 1000 object versions in a single GET request
- Using batch delete API, delete 1000 at a time
- Repeat it till the objects in the prefix are empty

3. Create and schedule the EB rule to call the above Lambda three times in the same rule with input as bucket_name and prefixes_list for every 15/16 minutes.

![s3_diagram drawio](https://user-images.githubusercontent.com/15073157/184546231-8a56f13e-01e9-4ec9-ad6b-68c397c2ca8d.png)

                       This figure illustrates the architecture of the solution proposed

# How to invoke the Lambda?
Create a Lambda function with the code in the file "lambda_function.py"

This function would take two parameters: bucket_name, prefix_list

Example : 
```
{'bucket_name': 'fill-in-the-bucket-name', 'prefix_list': "['prefix/1/1','prefix/2/2']"}
```

# Lambda to generate test objects
Another helper Lambda is creted to generate the test files for testing purposes.

Code is present in file s3_files_creation.py
This will take three parameters: bucket
Input:
```
{'bucket_name': 'your-bucket-name', 'bucket_paths': "['path/1/1/','path/1/2/']", 'no_of_files': 1000}
```



A detailed blog post [blog post](https://medium.com/@rapurukirity/deletion-of-millions-of-objects-from-versioning-enabled-aws-s3-822461437d41) is written, which would cover in-depth details, discussions and tests results.

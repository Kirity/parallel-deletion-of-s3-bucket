# Context
Deletion or empty of versioning enalbed AWS S3 bucket is a tedious job. 

There is no simple option to do in a single go especially if the bucket contains millions of files(as on July-2022).

In this project a programatic approach is employed to do this job and we try to reach the maximum limits offered by the S3 to delete objects at full throttle.

# Solution

S3 allows up to 3500 write requests on each prefix in the S3 buckets with DELETE API.

The solution will use Lambda for the computing and EventBridge(EB) rules for the scheduling.

The complete solution looks as below:

1. Create a Lambda service role that has read and delete permission on the respective S3 bucket.

2. Write a Lambda function ```lambda_function.py```   with the following features:
- It takes bucket_name and prefixes_list as input
- Each prefix will create a sub-process
- Using the boto3 S3 client and using pagination, get 1000 object versions in a single GET request
- Using batch delete API, delete 1000 at a time
- Repeat it till the objects in the prefix are empty

3. Create and schedule the EB rule to call the above Lambda three times in the same rule with input as bucket_name and prefixes_list for every 15/16 minutes.

![s3_diagram drawio](https://user-images.githubusercontent.com/15073157/184546231-8a56f13e-01e9-4ec9-ad6b-68c397c2ca8d.png)

                       This figure illustrates the architecture of the solution proposed

# Discussion on the solution configurations:

**Why create a sub-process for each prefix?**

This is to take advantage of the vCPUs offered by Lambda. Thereby deletion would happen in parallel rather than in a serial way.

**Why fetch only 1000 object-version?**

A GET request supports a max of 1000 at a time, while pagination and batch delete only support up to 1000 at a time. Here, we are deleting 1000 objects (considering each version as an object) in a prefix at a time.

**Why call Lambda three times with a single with an EB rule?**

Since S3 supports up to 3500 deletes on a prefix, if we invoke the same Lambda three times with an EB rule, we are taking advantage of Lambda concurrency and achieving the rate of 3000 deletes. Currently, the EB rule supports up to five target invocations, but we go with three to stay within the throttling limits of S3.

**Why schedule for every 15/16 minutes in EB rule?**

This would automate the repeated invocations for every 15/16 min.

As Lambda’s maximum execution time is 15min, it would automatically stop execution after 15min. Therefore an option is to automate the triggering of the Lambda in a loop until all the objects are entirely deleted. Scheduling every 16min is to ensure that there would not be more than three concurrent invocations at any given time in order not to overwhelm S3(to avoid throttling exceptions).


**How much should the timeout value be for the Lambda function?**

Set it to the maximum allowed value i.e., 15 min.


**How many vCPUs should be configured to the Lambda?**

The only way to increase/decrease the CPUs is to increase/decrease the memory setting. One can set memory between 128–10240 MB, and Lambda will allocate a vCPUs proposal to the set memory.

Set the memory to the maximum allowed value, i.e., 10240 MB thereby, the allocated vCPUs would be six.

**How many S3 prefixes be used to invoke S3 Lambda from EB?**

Since Lambda only supports a maximum of six vCPUs, it would be ideal to utilize six prefixes.

The idea is to create six threads in the Lambda for the six input prefixes.


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

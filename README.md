# lambda-parallel-deletion-of-s3-buecket
This project is an AWS Lambda function, which is used to delete the objects from an versioning enabled bucket

# How to run?
Create a Lambda function with the code in the file "lambda_function.py"

This function would take two parameters: bucket_name, prefix_list

Example : 
```
{'bucket_name': 'fill-in-the-bucket-name', 'prefix_list': "['prefix/1/1','prefix/2/2']"}
```

Detailed explantion can found in this [blog post](https://medium.com/@rapurukirity/deletion-of-millions-of-objects-from-versioning-enabled-aws-s3-822461437d41)

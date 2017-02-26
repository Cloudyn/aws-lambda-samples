# AWS Lambda Samples

aws-lambda-samples demonstrates integrating AWS Lambda Service with Cloudyn use cases.
As with any code, please test before using in production.

## Table of contents

* [python-stop-instances.py](#python-stop-instances)

## Python Stop Instances

Stop Instances triggered by a Cloudyn scheduled report

1. Create a Cloudyn report with the required filter (filter should include the matching account name).
2. Schedule this report to an S3 bucket in the relevant account (use a distinct file prefix).
3. Create a new lambda function (python 2.7) triggered by the relevant report creation in S3 (see http://docs.aws.amazon.com/lambda/latest/dg/with-s3.html for details)
4. Copy the code from [python-stop-instances.py](python-stop-instances.py)

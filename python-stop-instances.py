from __future__ import print_function
import urllib
import boto3
import csv
import codecs


def get_bucket_and_filename(record):
    """Extract S3 Bucket Name and File Name from event record"""
    try:
        bucket = record['s3']['bucket']['name']
        key = urllib.unquote_plus(record['s3']['object']['key'])
    except KeyError as ke:
        print('Failed to retrieve bucket or filename, KeyError:', ke)
        raise
    except Exception as e:
        print('Failed to retrieve bucket or filename, Exception:', e)
        raise
    return bucket, key


def get_csvfile(record):
    """Get csv file stream from S3"""
    try:
        bucket, key = get_bucket_and_filename(record)
        s3 = boto3.resource('s3')
        csvfile = s3.ObjectSummary(bucket, key).get()
        print("csvfile: ", csvfile)
    except Exception as e:
        print('Failed to get csv file, Exception:', e)
        raise
    return csvfile


def get_instances(csvfile, idcolumn='InstanceID', regioncolumn='Region'):
    """Get Instance IDs by Regions from csv
       Return a dictionary in the format {Region: [InstanceId, InstanceId, ...], ...}
       e.g. {'us-west-2': ['i-01234567'], 'us-east-1': ['i-01234568', 'i-01234569', 'i-01234570']}"""
    try:
        csvreader = csv.DictReader(codecs.getreader('utf-8')(csvfile['Body']))
        # get Instance IDs and Regions
        instances = {}
        for row in csvreader:
            # print("row: ", row)
            if not row[regioncolumn] in instances:
                instances[row[regioncolumn]] = []
            instances[row[regioncolumn]].append(row[idcolumn])
    except Exception as e:
        print('Failed to retrieve instance ids, Exception:', e)
        raise
    return instances


def stop_instances(instances):
    """stop Instances by ids and regions"""
    for region in instances:
        print(region, instances[region])
        try:
            ec2 = boto3.client('ec2', region)
            ec2.stop_instances(InstanceIds=instances[region])
            print('stopped instances: ', str(instances[region]))
        except Exception as e:
            print('Failed to stop instances, Exception:', e)
            raise


def lambda_handler(event, context):
    for record in event['Records']:
        try:
            csvfile = get_csvfile(record)
            instances = get_instances(csvfile)
            print('instances: ', instances)
            stop_instances(instances)
        except Exception:
            continue

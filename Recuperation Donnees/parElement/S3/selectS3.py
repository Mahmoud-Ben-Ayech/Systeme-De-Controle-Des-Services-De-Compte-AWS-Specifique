import boto3
import datetime
import pymongo

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["BucketS3"]

myTable.delete_many({})

def get_s3_size(cloudwatch_client,buckName):
    size_in_mb=0
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/S3',
        MetricName='BucketSizeBytes',
        Dimensions=[
            {
                'Name': 'BucketName',
                'Value': buckName
            },
            {
                'Name': 'StorageType',
                'Value': 'StandardStorage'
            }
        ],
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=2),
        EndTime=datetime.datetime.utcnow(),
        Statistics=['Average'],
        Period=86400
    )
    if 'Datapoints' in response and len(response['Datapoints']) > 0:
        size_in_bytes = response['Datapoints'][0]['Average']
        size_in_mb=round(size_in_bytes/(1024 ** 2),3)   
    return  size_in_mb        


client = boto3.client("s3")
response=client.list_buckets()
buckets=response['Buckets']
cloudwatch_client = boto3.client('cloudwatch')
count_id=1
s3Tab=[]
for buck in buckets:
    loc=client.get_bucket_location(Bucket=buck['Name'])
    bucket_reg=loc['LocationConstraint'] if 'LocationConstraint' in loc and loc['LocationConstraint'] else 'us-east-1'
    bucket_size_Mb=get_s3_size(cloudwatch_client,buck['Name'])
    s3Tab.append({'_id':count_id,'REGION':bucket_reg,'Bucket Name':buck['Name'],'Creation Date':buck['CreationDate'],'TailleMB':bucket_size_Mb})
    count_id+=1
myTable.insert_many(s3Tab)        



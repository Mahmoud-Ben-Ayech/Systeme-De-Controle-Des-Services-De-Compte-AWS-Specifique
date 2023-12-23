import boto3
import pymongo

client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["Snapshot"]

myTable.delete_many({})
count_id=1
snapTab=[]
for reg in list_Regions:
    cl = boto3.client('ec2', region_name=reg)
    response=cl.describe_snapshots(OwnerIds=['self'])
    snapshots=response['Snapshots']
    for snap in snapshots:
        snapTab.append({'_id':count_id,'REGION':reg,'Id':snap['SnapshotId'],'Taille GB':snap['VolumeSize'],
                        'Progress':snap['Progress'],'State':snap['State']})
        count_id+=1
myTable.insert_many(snapTab)            

import boto3
import pymongo
client=boto3.client(service_name='ec2')
all_regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["Subnets"]

myTable.delete_many({})
count_id=1
subnetTab=[]
for reg in list_Regions :
    cl=boto3.client("ec2",region_name=reg)
    response=cl.describe_subnets()
    for sub in response['Subnets']:
        subnetTab.append({'_id':count_id,'REGION':reg,'Id':sub['SubnetId'],'VPC Id':sub['VpcId'],
                          'Availability Zone':sub['AvailabilityZone'],'State':sub['State']}) 
        count_id+=1

myTable.insert_many(subnetTab)        

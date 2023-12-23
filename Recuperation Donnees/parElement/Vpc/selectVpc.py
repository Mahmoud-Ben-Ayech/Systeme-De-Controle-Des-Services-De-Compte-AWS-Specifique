import boto3
import pymongo
client=boto3.client(service_name='ec2')
all_regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["Vpc"]

myTable.delete_many({})
count_id=1
vpcTab=[]  
for reg in list_Regions :
    cl=boto3.client("ec2",region_name=reg)
    response=cl.describe_vpcs()
    for vpc in response['Vpcs'] :
        vpcTab.append({'_id':count_id,'REGION':reg,'Id':vpc["VpcId"],'Instance Tenancy':vpc["InstanceTenancy"],'State':vpc["State"]})
        count_id+=1
myTable.insert_many(vpcTab)  
    
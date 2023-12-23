import boto3
import pymongo

client=boto3.client(service_name='ec2')
all_regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["InternetGetway"]

myTable.delete_many({})
count_id=1
igwTab=[]
for reg in list_Regions :       
    cl=boto3.client("ec2",region_name=reg)
    response=cl.describe_internet_gateways()
    for igw in response['InternetGateways']:
        if 'Attachments' in igw and len(igw['Attachments'])>0 :
            state_igw=igw['Attachments'][0]['State']
            vpcId_igw=igw['Attachments'][0]['VpcId']
        else :
            state_igw='NOT Available' 
            vpcId_igw='NOT Attached'
        igwTab.append({'_id':count_id,'REGION':reg,'Id':igw['InternetGatewayId'],'VPC Id':vpcId_igw,'State':state_igw})
        count_id+=1
myTable.insert_many(igwTab) 







import boto3
import pymongo

client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["Ami"]

myTable.delete_many({})
count_id=1
amiTab=[]
for reg in list_Regions:
    cl=boto3.client('ec2',region_name=reg)
    response=cl.describe_images(Owners=['self'])
    for ami in response['Images']:
        amiTab.append({'_id':count_id,'REGION':reg,'AMI Name':ami['Name'],'ID':ami['ImageId'],'Creation Date':ami['CreationDate'],
                       'Platform':ami['PlatformDetails'],'State':ami['State']})
        count_id+=1
myTable.insert_many(amiTab) 

import boto3
import pymongo 

client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["Rds"]

myTable.delete_many({})
count_id=1
RdsTab=[]
for reg in list_Regions :
    clientRds = boto3.client('rds',region_name=reg)
    res=clientRds.describe_db_instances()
    for db in res['DBInstances']:
        RdsTab.append({'_id':count_id,'REGION':reg,'RDS Identifier':db['DBInstanceIdentifier'],'Size':db['DBInstanceClass'],
                     'Engine':db['Engine'],'Availability Zone':db['AvailabilityZone'],
                     'Creation Date':db['InstanceCreateTime'],'Status':db['DBInstanceStatus']})
        count_id+=1
myTable.insert_many(RdsTab)            



















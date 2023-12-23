import boto3
import pymongo

client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["instanceEc2"]

myTable.delete_many({})
count_id=1                 
instancesTab=[]
for region in list_Regions :
    instances = boto3.resource('ec2', region_name=region).instances.all()
    for instance in instances:
        if instance.tags :
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
                    break
        else :
            instance_name="no specific tag"  
        instancesTab.append({'_id':count_id,'REGION':region,'instance ID':instance.id,'Instance Name':instance_name,
                             'AMI':instance.image.id,'Type':instance.instance_type,'IPv4 Address':instance.public_ip_address,
                             'Launch Time':instance.launch_time,'State':instance.state["Name"]})  
        count_id+=1
myTable.insert_many(instancesTab) 


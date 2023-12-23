import boto3
import pymongo

client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["ElasticIp"]

myTable.delete_many({})
count_id=1
eipTab=[]
for reg in list_Regions :
    cl = boto3.client('ec2',region_name=reg)
    addresses_dict = cl.describe_addresses()
    for eip_dict in addresses_dict['Addresses']:
        if 'Tags' in eip_dict :
            eip_name=eip_dict['Tags'][0]['Value']
        else :
            eip_name='no tags'    
        eipTab.append({'_id':count_id,'REGION':reg,'Name':eip_name,'Domaine':eip_dict['Domain'],
                       'Public Ip':eip_dict['PublicIp'],'Private Ip address':eip_dict['PrivateIpAddress']})
        count_id+=1
myTable.insert_many(eipTab)        


       
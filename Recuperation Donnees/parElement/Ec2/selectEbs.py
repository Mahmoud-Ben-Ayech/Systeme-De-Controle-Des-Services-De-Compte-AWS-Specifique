import boto3
import pymongo

client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["Ebs"]

myTable.delete_many({})
count_id=1
ebsTab=[]
for reg in list_Regions:
   cl = boto3.client('ec2', region_name=reg)
   response=cl.describe_volumes()
   volumes=response['Volumes']
   for volume in volumes:
      if 'Tags' in volume :
         name_ebs=volume['Tags'][0]['Value']       
      else :
         name_ebs='No Tags'  
      ebsTab.append({'_id':count_id,'REGION':reg,'Volume Name':name_ebs,'Id':volume['VolumeId'],
                     'Created Time':volume['CreateTime'],'Taille GB':volume['Size'],
                     'State':volume['State']})
      count_id+=1
myTable.insert_many(ebsTab) 


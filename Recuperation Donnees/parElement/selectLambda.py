import boto3
import pymongo
client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["LambdaFunctions"]

myTable.delete_many({})
count_id=1
LmbTab=[]
for reg in list_Regions:
   cl=boto3.client("lambda",region_name=reg)
   response=cl.list_functions()
   for f in response['Functions']:
      config_fonc=cl.get_function(FunctionName=f['FunctionName'])['Configuration']
      taille_fct=config_fonc['CodeSize']
      etat_fct=config_fonc['State']
      LmbTab.append({'_id':count_id,'REGION':reg,'Name':f['FunctionName'],'Runtime':f['Runtime'],
                     'Last Modified':f['LastModified'],'Taille Byte':taille_fct,'State':etat_fct})
      count_id+=1
myTable.insert_many(LmbTab)          

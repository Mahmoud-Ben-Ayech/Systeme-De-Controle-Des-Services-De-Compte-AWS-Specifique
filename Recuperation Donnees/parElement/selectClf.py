import boto3
import pymongo 
client = boto3.client("cloudfront")
response = client.list_distributions()

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["CloudFront"]

myTable.delete_many({})
count_id=1
ClfTab=[]
for dist in response["DistributionList"]["Items"]:
    if 'Aliases' in dist:
        alternate_domaine=dist['Aliases']['Items'][0]
    else :
        alternate_domaine='Not Attached'    

    ClfTab.append({'_id':count_id,'Id':dist['Id'],'Alternate Domaine':alternate_domaine,
                    'Last Modified':dist['LastModifiedTime'],'State':dist['Status']})
    count_id+=1
myTable.insert_many(ClfTab)

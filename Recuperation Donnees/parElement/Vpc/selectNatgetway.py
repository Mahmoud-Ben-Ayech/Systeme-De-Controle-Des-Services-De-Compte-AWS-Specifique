import boto3
import pymongo
client=boto3.client(service_name='ec2')
all_regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["NatGetway"]

myTable.delete_many({})
count_id=1
ngetwayTab=[]
for reg in list_Regions :
    cl=boto3.client("ec2",region_name=reg)
    response=cl.describe_nat_gateways()
    for ngetw in response['NatGateways']:
        if 'Tags' in ngetw :
            ngetw_name=ngetw['Tags'][0]['Value']
        else :    
            ngetw_name='No specific Tag'
        ngetwayTab.append({'_id':count_id,'REGION':reg,'Name':ngetw_name,'Nat Getway Id':ngetw['NatGatewayId'],
                            'Vpc Id':ngetw['VpcId'],'Created Time':ngetw['CreateTime'],
                            'State':ngetw['State']})
        count_id+=1
myTable.insert_many(ngetwayTab)   

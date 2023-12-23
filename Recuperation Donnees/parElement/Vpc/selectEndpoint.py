import boto3
import pymongo
client=boto3.client(service_name='ec2')
all_regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["VpcEndpoint"]

myTable.delete_many({})
count_id=1
epointTab=[]
for reg in list_Regions :
    cl=boto3.client("ec2",region_name=reg)
    response=cl.describe_vpc_endpoints()
    for vpcend in response['VpcEndpoints']:
        if 'Tags' in vpcend :
            epoint_name=vpcend['Tags'][0]['Value']
        else :
            epoint_name='No Specific Tag'
        epointTab.append({'_id':count_id,'REGION':reg,'Name':epoint_name,'VPC ENDPOINT Id':vpcend['VpcEndpointId'],
                            'Vpc Id':vpcend['VpcId'],'Type':vpcend['VpcEndpointType'],
                            'Created Time':vpcend['CreationTimestamp'],'State':vpcend['State']})  
        count_id+=1
myTable.insert_many(epointTab)   

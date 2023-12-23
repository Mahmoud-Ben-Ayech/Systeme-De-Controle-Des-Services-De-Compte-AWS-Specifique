import boto3
import pymongo
client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["TaskDefinition"]

myTable.delete_many({})
count_id=1
tdefTab=[]
for reg in list_Regions :
    clientEcs = boto3.client('ecs',region_name=reg)
    response=clientEcs.list_task_definitions()
    while 1 :
        for taskDefArn in response['taskDefinitionArns']:
            taskDef_info=clientEcs.describe_task_definition(taskDefinition=taskDefArn)
            task_definition = taskDef_info['taskDefinition']
            tdefTab.append({'_id':count_id,'REGION':reg,'Task Definition':task_definition['family'],'Status Last Version':task_definition['status']})
            count_id+=1
        if  'nextToken' in response  :
            response=clientEcs.list_task_definitions(nextToken=response['nextToken'])   
        else :
            break 
myTable.insert_many(tdefTab) 


   

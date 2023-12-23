import boto3
import pymongo
client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["EcsClusters"]

myTable.delete_many({})
count_id=1
ecsTab=[]
for reg in list_Regions :
    clientEcs = boto3.client('ecs',region_name=reg)
    response=clientEcs.list_clusters()
    for clusterArn in response['clusterArns']:
        cluster_info = clientEcs.describe_clusters(clusters=[clusterArn])
        cluster = cluster_info['clusters'][0]
        ecsTab.append({'_id':count_id,'REGION':reg,'Cluster Name':cluster['clusterName'],'Active Services':cluster['activeServicesCount'],
                        'Running Tasks':cluster['runningTasksCount'],'Pending Tasks':cluster['pendingTasksCount']})
        count_id+=1
myTable.insert_many(ecsTab) 

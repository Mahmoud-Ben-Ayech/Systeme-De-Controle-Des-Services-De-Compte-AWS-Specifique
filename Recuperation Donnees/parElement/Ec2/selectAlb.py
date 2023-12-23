import boto3
import pymongo

client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]
myTable = myDb["alb"]

myTable.delete_many({})

def gettargetgroups(arn,alb):
    tgs = alb.describe_target_groups(LoadBalancerArn=arn)
    tgstring = [tg["TargetGroupName"] for tg in tgs["TargetGroups"]]
    return tgstring 
count_id=1
albTab=[]
for region in list_Regions :   
    alb = boto3.client('elbv2',region_name=region)
    lbs = alb.describe_load_balancers(PageSize=400)
    for lb in lbs["LoadBalancers"]:
        albTab.append({'_id':count_id,'REGION':region,'ALb Name':lb["LoadBalancerName"],
                        'Type':lb["Type"],'Target Groupe':str(gettargetgroups(lb["LoadBalancerArn"],alb)),
                        'State':lb["State"]["Code"]})
        count_id+=1
myTable.insert_many(albTab) 

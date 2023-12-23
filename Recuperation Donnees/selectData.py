import boto3
import pymongo 
import datetime

#Selection des Regions 

client=boto3.client(service_name='ec2')
all_Regions=client.describe_regions()
list_Regions=[e['RegionName'] for e in all_Regions['Regions']]

#Connexion avec BDD & fonctions partagées 

client = pymongo.MongoClient('localhost',27017)
myDb = client["mydb"]

def resetTable(myTable):
    myTable.delete_many({})
def insertTable(myTable,dTab):
    if dTab:
        myTable.insert_many(dTab)

#                                      **********************************   PARTIE EC2   ******************************************

#Partie Instances Ec2  


def selectInstances() :
    myTable = myDb["instanceEc2"]
    resetTable(myTable)
    instancesTab=[]
    count_id_instance=1
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
            instancesTab.append({'_id':count_id_instance,'REGION':region,'instance ID':instance.id,'Instance Name':instance_name,
                                'AMI':instance.image.id,'Type':instance.instance_type,'IPv4 Address':instance.public_ip_address,
                                'Launch Time':instance.launch_time,'State':instance.state["Name"]})  
            count_id_instance+=1       
    insertTable(myTable,instancesTab)       
          



#partie APPLICATION LOAD BALANCERS (ALBs)
    

def gettargetgroups(arn,alb):
    tgs = alb.describe_target_groups(LoadBalancerArn=arn)
    tgstring = [tg["TargetGroupName"] for tg in tgs["TargetGroups"]]
    return tgstring   

def selectAlb() :
    myTable = myDb["alb"]
    resetTable(myTable)
    albTab=[]
    count_id_alb=1
    for region in list_Regions :   
        alb = boto3.client('elbv2',region_name=region)
        lbs = alb.describe_load_balancers(PageSize=400)
        for lb in lbs["LoadBalancers"]:
            albTab.append({'_id':count_id_alb,'REGION':region,'ALb Name':lb["LoadBalancerName"],
                        'Type':lb["Type"],'Target Groupe':str(gettargetgroups(lb["LoadBalancerArn"],alb)),
                        'State':lb["State"]["Code"]})
            count_id_alb+=1           
    insertTable(myTable,albTab)    


#Partie AMAZONE MACHINE IMAGES  (AMIs)

def selectAmi() :
    myTable = myDb["Ami"]
    resetTable(myTable)
    amiTab=[]
    count_id_ami=1
    for reg in list_Regions:
        cl=boto3.client('ec2',region_name=reg)
        response=cl.describe_images(Owners=['self'])
        for ami in response['Images']:
            amiTab.append({'_id':count_id_ami,'REGION':reg,'AMI Name':ami['Name'],'ID':ami['ImageId'],'Creation Date':ami['CreationDate'],
                          'Platform':ami['PlatformDetails'],'State':ami['State']})
            count_id_ami+=1           
    insertTable(myTable,amiTab)  


#Partie ELASTIC BLOCK STORAGE (EBS) 

def selectEbs() :
    myTable = myDb["Ebs"]
    resetTable(myTable)
    ebsTab=[]
    count_id_ebs=1
    for reg in list_Regions:
        cl = boto3.client('ec2', region_name=reg)
        response=cl.describe_volumes()
        volumes=response['Volumes']
        for volume in volumes:
            if 'Tags' in volume :
                name_ebs=volume['Tags'][0]['Value']       
            else :
                name_ebs='No Tags'  
            ebsTab.append({'_id':count_id_ebs,'REGION':reg,'Volume Name':name_ebs,'Id':volume['VolumeId'],
                          'Created Time':volume['CreateTime'],'Taille GB':volume['Size'],
                          'State':volume['State']})
            count_id_ebs+=1            
    insertTable(myTable,ebsTab)

#Partie Snapshot (SNAP)

def selectSnap() :
    myTable = myDb["Snapshot"]
    resetTable(myTable)
    snapTab=[]
    count_id_snap=1
    for reg in list_Regions:
        cl = boto3.client('ec2', region_name=reg)
        response=cl.describe_snapshots(OwnerIds=['self'])
        snapshots=response['Snapshots']
        for snap in snapshots:
            snapTab.append({'_id':count_id_snap,'REGION':reg,'Id':snap['SnapshotId'],'Taille GB':snap['VolumeSize'],
                           'Progress':snap['Progress'],'State':snap['State']})
            count_id_snap+=1            
    insertTable(myTable,snapTab) 

#Partie Elastic Ip (EIP)

def selectEip() :
    myTable = myDb["ElasticIp"]
    resetTable(myTable)
    eipTab=[]
    count_id_eip=1
    for reg in list_Regions :
        cl = boto3.client('ec2',region_name=reg)
        addresses_dict = cl.describe_addresses()
        for eip_dict in addresses_dict['Addresses']:
            if 'Tags' in eip_dict :
                eip_name=eip_dict['Tags'][0]['Value']
            else :
                eip_name='no tags'    
            eipTab.append({'_id':count_id_eip,'REGION':reg,'Name':eip_name,'Domaine':eip_dict['Domain'],
                          'Public Ip':eip_dict['PublicIp'],'Private Ip address':eip_dict['PrivateIpAddress']})
            count_id_eip+=1           
    insertTable(myTable,eipTab)  


#                                         ************************************** PARTIE Buckets S3  *********************************************

#Partie Buckets S3 


def get_s3_size(cloudwatch_client,buckName):
    size_in_mb=0
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/S3',
        MetricName='BucketSizeBytes',
        Dimensions=[
            {
                'Name': 'BucketName',
                'Value': buckName
            },
            {
                'Name': 'StorageType',
                'Value': 'StandardStorage'
            }
        ],
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=2),
        EndTime=datetime.datetime.utcnow(),
        Statistics=['Average'],
        Period=86400
    )
    if 'Datapoints' in response and len(response['Datapoints']) > 0:
        size_in_bytes = response['Datapoints'][0]['Average']
        size_in_mb=round(size_in_bytes/(1024 ** 2),3)   
    return  size_in_mb        

def selectS3() :
    myTable = myDb["BucketS3"]
    resetTable(myTable)
    client = boto3.client("s3")
    response=client.list_buckets()
    buckets=response['Buckets']
    cloudwatch_client = boto3.client('cloudwatch')
    s3Tab=[]
    count_id_s3=1
    for buck in buckets:
        loc=client.get_bucket_location(Bucket=buck['Name'])
        bucket_reg=loc['LocationConstraint'] if 'LocationConstraint' in loc and loc['LocationConstraint'] else 'us-east-1'
        bucket_size_Mb=get_s3_size(cloudwatch_client,buck['Name'])
        s3Tab.append({'_id':count_id_s3,'REGION':bucket_reg,'Bucket Name':buck['Name'],'Creation Date':buck['CreationDate'],'TailleMB':bucket_size_Mb})
        count_id_s3+=1        
    insertTable(myTable,s3Tab)


#                                       ******************************************** PARTIE RDS  ***********************************************

#Partie Relational Database (Rds)


def selectRds() :
    myTable = myDb["Rds"]
    resetTable(myTable)
    RdsTab=[]
    count_id_rds=1
    for reg in list_Regions :
        clientRds = boto3.client('rds',region_name=reg)
        res=clientRds.describe_db_instances()
        for db in res['DBInstances']:
            RdsTab.append({'_id':count_id_rds,'REGION':reg,'RDS Identifier':db['DBInstanceIdentifier'],'Size':db['DBInstanceClass'],
                          'Engine':db['Engine'],'Availability Zone':db['AvailabilityZone'],
                          'Creation Date':db['InstanceCreateTime'],'Status':db['DBInstanceStatus']})
            count_id_rds+=1
    insertTable(myTable,RdsTab)

#                                            ******************************************  PARTIE CloudFront  **********************************************

#Partie CloudFront


def selectClf() :
    myTable = myDb["CloudFront"]
    resetTable(myTable)
    client = boto3.client("cloudfront")
    response = client.list_distributions()
    ClfTab=[]
    count_id_clf=1
    for dist in response["DistributionList"]["Items"]:
        if 'Aliases' in dist:
            alternate_domaine=dist['Aliases']['Items'][0]
        else :
            alternate_domaine='Not Attached'    
        ClfTab.append({'_id':count_id_clf,'Id':dist['Id'],'Alternate Domaine':alternate_domaine,
                      'Last Modified':dist['LastModifiedTime'],'State':dist['Status']})
        count_id_clf+=1
    insertTable(myTable,ClfTab)

#                                              ***************************************  PARTIE Fonctions Lambda *************************************************

#Partie Lambda 


def selectLmb() :
    myTable = myDb["LambdaFunctions"]
    resetTable(myTable)
    LmbTab=[]
    count_id_lmb=1
    for reg in list_Regions:
       cl=boto3.client("lambda",region_name=reg)
       response=cl.list_functions()
       for f in response['Functions']:
          config_fonc=cl.get_function(FunctionName=f['FunctionName'])['Configuration']
          taille_fct=config_fonc['CodeSize']
          etat_fct=config_fonc['State']
          LmbTab.append({'_id':count_id_lmb,'REGION':reg,'Name':f['FunctionName'],'Runtime':f['Runtime'],
                     'Last Modified':f['LastModified'],'Taille Byte':taille_fct,'State':etat_fct})
          count_id_lmb+=1
    insertTable(myTable,LmbTab) 


#                                              *************************************** Partie Vpc  ***************************************


#Recuperation de VPCs


def selectVpc():
  myTable = myDb["Vpc"]
  resetTable(myTable)
  vpcTab=[]  
  count_id_vpc=1
  for reg in list_Regions :
    cl=boto3.client("ec2",region_name=reg)
    response=cl.describe_vpcs()
    for vpc in response['Vpcs'] :
        vpcTab.append({'_id':count_id_vpc,'REGION':reg,'Id':vpc["VpcId"],'Instance Tenancy':vpc["InstanceTenancy"],'State':vpc["State"]})
        count_id_vpc+=1        
  insertTable(myTable,vpcTab)  


# partie Subnets 

def selectSubnet() :
  myTable = myDb["Subnets"]
  resetTable(myTable)
  subnetTab=[]
  count_id_subnet=1
  for reg in list_Regions :
    cl=boto3.client("ec2",region_name=reg)
    response=cl.describe_subnets()
    for sub in response['Subnets']:
        subnetTab.append({'_id':count_id_subnet,'REGION':reg,'Id':sub['SubnetId'],'VPC Id':sub['VpcId'],
                          'Availability Zone':sub['AvailabilityZone'],'State':sub['State']}) 
        count_id_subnet+=1       
  insertTable(myTable,subnetTab)


#Partie Internet GetWay

def selectIGWay() :
    myTable = myDb["InternetGetway"]
    resetTable(myTable)
    igwTab=[]
    count_id_igway=1
    for reg in list_Regions :
        cl=boto3.client("ec2",region_name=reg)
        response=cl.describe_internet_gateways()
        for igw in response['InternetGateways']:
            if 'Attachments' in igw and len(igw['Attachments'])>0 :
                state_igw=igw['Attachments'][0]['State']
                vpcId_igw=igw['Attachments'][0]['VpcId']
            else :
                state_igw='NOT Available' 
                vpcId_igw='NOT Attached'
            igwTab.append({'_id':count_id_igway,'REGION':reg,'Id':igw['InternetGatewayId'],'VPC Id':vpcId_igw,'State':state_igw})
            count_id_igway+=1
    insertTable(myTable,igwTab)


# Partie Endpoint Vpc 


def selectEpoint() :
    myTable = myDb["VpcEndpoint"]
    resetTable(myTable)
    epointTab=[]
    count_id_epoint=1
    for reg in list_Regions :
         cl=boto3.client("ec2",region_name=reg)
         response=cl.describe_vpc_endpoints()
         for vpcend in response['VpcEndpoints']:
            if 'Tags' in vpcend :
                epoint_name=vpcend['Tags'][0]['Value']
            else :
                epoint_name='No Specific Tag'
            epointTab.append({'_id':count_id_epoint,'REGION':reg,'Name':epoint_name,'VPC ENDPOINT Id':vpcend['VpcEndpointId'],
                            'Vpc Id':vpcend['VpcId'],'Type':vpcend['VpcEndpointType'],
                            'Created Time':vpcend['CreationTimestamp'],'State':vpcend['State']}) 
            count_id_epoint+=1
    insertTable(myTable,epointTab)  


#Partie Nat Getway 


def selectNgetway() :
    myTable = myDb["NatGetway"]
    resetTable(myTable)
    ngetwayTab=[]
    count_id_ngway=1
    for reg in list_Regions :
         cl=boto3.client("ec2",region_name=reg)
         response=cl.describe_nat_gateways()
         for ngetw in response['NatGateways']:
            if 'Tags' in ngetw :
                ngetw_name=ngetw['Tags'][0]['Value']
            else :    
                ngetw_name='No specific Tag'
            ngetwayTab.append({'_id':count_id_ngway,'REGION':reg,'Name':ngetw_name,'Nat Getway Id':ngetw['NatGatewayId'],
                            'Vpc Id':ngetw['VpcId'],'Created Time':ngetw['CreateTime'],
                            'State':ngetw['State']})
            count_id_ngway+=1
    insertTable(myTable,ngetwayTab)  


#                                             *************************  Partie ECS  **************************************************


#Partie Clusters 


def selectEcs():
    myTable = myDb["EcsClusters"]
    resetTable(myTable)
    ecsTab=[]
    count_id_ecs=1
    for reg in list_Regions :
        clientEcs = boto3.client('ecs',region_name=reg)
        response=clientEcs.list_clusters()
        for clusterArn in response['clusterArns']:
            cluster_info = clientEcs.describe_clusters(clusters=[clusterArn])
            cluster = cluster_info['clusters'][0]
            ecsTab.append({'_id':count_id_ecs,'REGION':reg,'Cluster Name':cluster['clusterName'],'Active Services':cluster['activeServicesCount'],
                        'Running Tasks':cluster['runningTasksCount'],'Pending Tasks':cluster['pendingTasksCount']})
            count_id_ecs+=1
    insertTable(myTable,ecsTab) 


#Partie Task Definition 


def selectTdef() :
    myTable = myDb["TaskDefinition"]
    resetTable(myTable)
    tdefTab=[]
    count_id_tdef=1
    for reg in list_Regions :
        clientEcs = boto3.client('ecs',region_name=reg)
        response=clientEcs.list_task_definitions()
        while 1 :
            for taskDefArn in response['taskDefinitionArns']:
               taskDef_info=clientEcs.describe_task_definition(taskDefinition=taskDefArn)
               task_definition = taskDef_info['taskDefinition']
               tdefTab.append({'_id':count_id_tdef,'REGION':reg,'Task Definition':task_definition['family'],'Status Last Version':task_definition['status']})
               count_id_tdef+=1
            if  'nextToken' in response  :
                response=clientEcs.list_task_definitions(nextToken=response['nextToken'])   
            else :
                break 
    insertTable(myTable,tdefTab)



#                                             ********************************  Configuration Des Paths  **********************************************************

#Organisation des parties 


dict_ec2={'instancesEc2':selectInstances(),'alb':selectAlb(),'ami':selectAmi(),
      'ebs':selectEbs(),'snap':selectSnap(),'eip':selectEip()}

dict_s3={'s3':selectS3()}

dict_rds={'rds':selectRds()}

dict_clf={'clf':selectClf()}

dict_lmbda={'lambda':selectLmb()}

dict_vpc={'vpc':selectVpc(),'subnet':selectSubnet(),
      'internetGetway':selectIGWay(),'endpoint':selectEpoint(),'natGetway':selectNgetway()}

dict_ecs={'ecs':selectEcs(),'taskDef':selectTdef()}


all_services=[dict_ec2,
              dict_s3,
              dict_rds,
              dict_clf,
              dict_lmbda,
              dict_vpc,
              dict_ecs]   




#                                             ********************************* PARTIE MAIN   ************************************************************

#Executiion des fonctions dans tous les parties  

for service in all_services :
    path=list(service.keys())
    for d in path :
        service[d]


       
from app import app
from app.shared_functions import get_all_data,search_data



# Instances Ec2 

ec2_table_name='instanceEc2'

@app.route('/ec2/getAll')
def getAllInstances():
    return get_all_data(ec2_table_name)

@app.route('/ec2/search/<instance_name>')
def get_instance(instance_name):
    return search_data(ec2_table_name,instance_name,'Instance Name')
     

#Alb 

alb_table_name='alb'

@app.route('/alb/getAll')
def getAllAlb():
    return get_all_data(alb_table_name)

@app.route('/alb/search/<alb_name>')
def get_alb(alb_name):
    return search_data(alb_table_name,alb_name,'ALb Name')


#Ami 

ami_table_name='Ami'

@app.route('/ami/getAll')
def getAllAmi():
    return get_all_data(ami_table_name)

@app.route('/ami/search/<ami_name>')
def get_ami(ami_name):
    return search_data(ami_table_name,ami_name,'AMI Name')


#Ebs

ebs_table_name='Ebs'

@app.route('/ebs/getAll')
def getAllEbs():
    return get_all_data(ebs_table_name)

@app.route('/ebs/search/<ebs_name>')
def get_ebs(ebs_name):
    return search_data(ebs_table_name,ebs_name,'Volume Name')


#Snapshot

snap_table_name='Snapshot'

@app.route('/snapshot/getAll')
def getAllSnap():
    return get_all_data(snap_table_name)

@app.route('/snapshot/search/<state_id>')
def get_snap(state_id):
    return search_data(snap_table_name,state_id,'State')


#ElasticIp

eip_table_name='ElasticIp'

@app.route('/eip/getAll')
def getAllEip():
    return get_all_data(eip_table_name)

@app.route('/eip/search/<eip_name>')
def get_eip(eip_name):
    return search_data(eip_table_name,eip_name,'Name')
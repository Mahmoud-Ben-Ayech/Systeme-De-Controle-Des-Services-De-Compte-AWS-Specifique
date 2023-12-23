from app import app
from app.shared_functions import get_all_data,search_data




#Vpc

vpc_table_name='Vpc'

@app.route('/vpc/getAll')
def getAllVpc():
    return get_all_data(vpc_table_name)

@app.route('/vpc/search/<vpc_name>')
def get_vpc(vpc_name):
    return search_data(vpc_table_name,vpc_name,'State')


#Subnets

subnet_table_name='Subnets'

@app.route('/subnet/getAll')
def getAllSubnet():
    return get_all_data(subnet_table_name)

@app.route('/subnet/search/<sub_name>')
def get_subnet(sub_name):
    return search_data(subnet_table_name,sub_name,'State')


#Internet Getways

igtw_table_name='InternetGetway'

@app.route('/internetgetway/getAll')
def getAllIgetw():
    return get_all_data(igtw_table_name)

@app.route('/internetgetway/search/<igtw_name>')
def get_igtw(igtw_name):
    return search_data(igtw_table_name,igtw_name,'State')


#VpcEndpoint

endpoint_table_name='VpcEndpoint'

@app.route('/vpcendpoint/getAll')
def getAllEndpoint():
    return get_all_data(endpoint_table_name)

@app.route('/vpcendpoint/search/<endpoint_name>')
def get_endpoint(endpoint_name):
    return search_data(endpoint_table_name,endpoint_name,'Name')


#NatGetway

ngtw_table_name='NatGetway'

@app.route('/natgetway/getAll')
def getAllNgetw():
    return get_all_data(ngtw_table_name)

@app.route('/natgetway/search/<ngtw_name>')
def get_ngtw(ngtw_name):
    return search_data(ngtw_table_name,ngtw_name,'State')
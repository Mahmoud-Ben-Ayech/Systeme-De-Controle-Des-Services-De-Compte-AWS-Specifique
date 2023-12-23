from app import app
from app.shared_functions import get_all_data,search_data



#Rds

rds_table_name='Rds'

@app.route('/rds/getAll')
def getAllRds():
    return get_all_data(rds_table_name)

@app.route('/rds/search/<rds_name>')
def get_rds(rds_name):
    return search_data(rds_table_name,rds_name,'RDS Identifier')
from app import app
from app.shared_functions import get_all_data,search_data



#Lambda Functions

lmb_table_name='LambdaFunctions'

@app.route('/lambda/getAll')
def getAllLambda():
    return get_all_data(lmb_table_name)

@app.route('/lambda/search/<lmb_name>')
def get_lmb(lmb_name):
    return search_data(lmb_table_name,lmb_name,'Name')
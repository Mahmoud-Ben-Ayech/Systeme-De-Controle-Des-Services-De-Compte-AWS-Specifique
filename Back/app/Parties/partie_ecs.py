from app import app
from app.shared_functions import get_all_data,search_data



#Ecs Clusters

ecs_table_name='EcsClusters'

@app.route('/ecscluster/getAll')
def getAllEcs():
    return get_all_data(ecs_table_name)


#Task Definitions 

taskdef_table_name='TaskDefinition'

@app.route('/taskdef/getAll')
def getAllTaskDef():
    return get_all_data(taskdef_table_name)

@app.route('/taskdef/search/<tdef_name>')
def get_tdef(tdef_name):
    return search_data(taskdef_table_name,tdef_name,'Task Definition')
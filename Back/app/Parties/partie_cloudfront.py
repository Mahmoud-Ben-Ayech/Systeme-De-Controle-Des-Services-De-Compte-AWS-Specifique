from app import app
from app.shared_functions import get_all_data,search_data




#Cloud Front

clf_table_name='CloudFront'

@app.route('/cloudfront/getAll')
def getAllClf():
    return get_all_data(clf_table_name)

@app.route('/cloudfront/search/<clf_name>')
def get_clf(clf_name):
    return search_data(clf_table_name,clf_name,'Alternate Domaine')
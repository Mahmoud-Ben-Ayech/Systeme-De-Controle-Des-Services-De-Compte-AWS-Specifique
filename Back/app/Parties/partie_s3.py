from app import app
from app.shared_functions import get_all_data,search_data



#Bucket S3

s3_table_name='BucketS3'

@app.route('/s3/getAll')
def getAllS3():
    return get_all_data(s3_table_name)

@app.route('/s3/search/<buck_name>')
def get_s3(buck_name):
    return search_data(s3_table_name,buck_name,'Bucket Name')
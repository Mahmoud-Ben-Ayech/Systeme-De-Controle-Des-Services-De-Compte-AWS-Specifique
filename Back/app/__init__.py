from flask import Flask

from app.config_mail import Config
app = Flask(__name__)
app.config.from_object(Config)


from app import configuration,shared_functions,email_sender,config_mail
from app.Parties import partie_ec2,partie_cloudfront,partie_ecs
from app.Parties import partie_lambda,partie_rds,partie_s3,partie_vpc
from app.pages import Admin,User,SuperAdmin




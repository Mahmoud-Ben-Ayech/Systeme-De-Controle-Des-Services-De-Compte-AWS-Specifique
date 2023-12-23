from app import app
from flask import jsonify
import pymongo
import os






#            *********  Parametres de configurations (Variables d'environement )  ***********************

name_database=os.environ.get('NAME_DATABASE')  
if not name_database:
    name_database='mydb2'

temps_travail_Min=os.environ.get('TEMPS_DEBUT')
if not temps_travail_Min :
    temps_travail_Min='08:00:00'

temps_travail_Max=os.environ.get('TEMPS_FIN')
if not temps_travail_Max :
    temps_travail_Max='14:30:00'

jours_travail_list=os.environ.get('JOURS_TRAVAIL')
if jours_travail_list:
    jours_travail=jours_travail_list.split(',')
else :
    jours_travail=['Monday','Tuesday','Wednesday','Thursday','Friday']

taille_bucket_max=os.environ.get('TAILLE_BUCKET_MAX')
if not taille_bucket_max :
    taille_bucket_max=100

email_superadmin=os.environ.get('SUPER_EMAIL')  
if not email_superadmin:
    email_superadmin='mahmoud@gmail.com'

password_superadmin=os.environ.get('SUPER_PASSWORD')  
if not password_superadmin:
    password_superadmin='123456789'

 




@app.route('/varEnv/getDebut')
def getDebut():
    return temps_travail_Min

@app.route('/varEnv/getFin')
def getFin():
    return temps_travail_Max

@app.route('/varEnv/getJours')
def getJours():
    return jsonify(jours_travail)

@app.route('/varEnv/getTaille')
def getTaille():
    return jsonify(taille_bucket_max)

@app.route('/varEnv/getEmailSuper')
def getEmailSuper():
    return email_superadmin

@app.route('/varEnv/getPassSuper')
def getPassSuper():
    return password_superadmin

#Connexion a base de donnees 

client = pymongo.MongoClient('localhost',27017)
myDb = client[name_database]








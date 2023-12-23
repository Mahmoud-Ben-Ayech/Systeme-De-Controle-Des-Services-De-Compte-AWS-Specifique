from flask import jsonify
from app.configuration import myDb

#Fonction de recuperation de tous les donnees de table de BDD 
def get_all_data(table_name):
    myTable = myDb[table_name]
    return jsonify(list(myTable.find({})))

#Fonction de recherche via critere specifier dans la table de BDD 
def search_data(data_table_name,choice,critere_recherche):
    myTable=myDb[data_table_name]
    result=list(myTable.find({critere_recherche:choice}))
    return jsonify(result) 




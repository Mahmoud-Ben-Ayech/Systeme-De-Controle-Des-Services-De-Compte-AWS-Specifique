from app import app
from flask import request,jsonify
from app.configuration import myDb


@app.route("/getAdmins")
def getAdmins():
    admin_table=myDb["Admin"]
    return jsonify(list(admin_table.find({}))) 


@app.route("/addAdmin",methods=["POST"])
def addAdmin():
  try:  
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")

    admin_table=myDb["Admin"]
    admin_table.insert_one({"_id":email,"Email":email,'Password':password})      

    response = {"message": "Données reçues avec succès"}
    return jsonify(response), 200
  except Exception as e:
        response = {"error": str(e)}
        return jsonify(response), 400    
  
@app.route("/updateAdmin",methods=["POST"])
def updateAdmin():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")

    admin_table=myDb["Admin"]

    result=admin_table.update_one({"_id":email},{"$set":{"Email":email,'Password':password}})      

    if result.modified_count > 0:
        return "Mise à jour réussie", 200
    else:
        return "Aucun document mis à jour", 404
    
@app.route("/removeAdmin",methods=["POST"])
def removeAdmin():
    data=request.get_json()
    email=data.get("email")

    admin_table=myDb["Admin"]

    result=admin_table.delete_one({"_id":email})      

    if result.deleted_count > 0:
        return "Suppression réussie", 200
    else:
        return "Aucun document Supprimé!", 404   
from app import app
from flask import request,jsonify
from app.configuration import myDb


@app.route("/getUsers")
def getUsers():
    user_table=myDb["User"]
    return jsonify(list(user_table.find({}))) 


@app.route("/addUser",methods=["POST"])
def addUser():
  try:  
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")

    user_table=myDb["User"]
    user_table.insert_one({"_id":email,"Email":email,'Password':password})      

    response = {"message": "Données reçues avec succès"}
    return jsonify(response), 200
  except Exception as e:
        response = {"error": str(e)}
        return jsonify(response), 400
  
@app.route("/updateUser",methods=["POST"])
def updateUser():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")

    user_table=myDb["User"]

    result=user_table.update_one({"_id":email},{"$set":{"Email":email,'Password':password}})      

    if result.modified_count > 0:
        return "Mise à jour réussie", 200
    else:
        return "Aucun document mis à jour", 404
    
@app.route("/removeUser",methods=["POST"])
def removeUser():
    data=request.get_json()
    email=data.get("email")

    user_table=myDb["User"]

    result=user_table.delete_one({"_id":email})      

    if result.deleted_count > 0:
        return "Suppression réussie", 200
    else:
        return "Aucun document Supprimé!", 404    
    

@app.route("/updatePasswordAdmin",methods=["POST"])
def updatePasswordAdmin():
    data=request.get_json()
    email=data.get("email")
    oldPassword=data.get("oldPassword")
    newPassword=data.get("newPassword")

    admin_table=myDb["Admin"]
    getAdmin=admin_table.find_one({"_id":email})
    if getAdmin["Password"]==oldPassword :
        result=admin_table.update_one({"_id":email},{"$set":{"Email":email,'Password':newPassword}})      
    if result.modified_count > 0:
        return "Mise à jour réussie", 200
    else:
        return "Aucun document mis à jour", 404    
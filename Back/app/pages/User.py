from app import app
from flask import jsonify,request
from app.configuration import myDb



@app.route("/updatePasswordUser",methods=["POST"])
def updatePasswordUser():
    data=request.get_json()
    email=data.get("email")
    oldPassword=data.get("oldPassword")
    newPassword=data.get("newPassword")

    user_table=myDb["User"]
    getUser=user_table.find_one({"_id":email})
    if getUser["Password"]==oldPassword:
        result=user_table.update_one({"_id":email},{"$set":{"Email":email,'Password':newPassword}})      
    if result.modified_count > 0:
        return "Mise à jour réussie", 200
    else:
        return "Aucun document mis à jour", 404
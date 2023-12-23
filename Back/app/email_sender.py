from flask import request,jsonify
from flask_mail import Mail, Message
from app import app


mail = Mail(app)

@app.route('/send_email', methods=['POST','GET'])
def send_email():
  if request.method=='POST':  
    try:
        data=request.get_json()
        email=data.get("email")
        mess=data.get("message")

        msg=Message(" Mail Notification Application Dashboard De Compte AWS  ",recipients=[email])     
        msg.body=mess

        mail.send(msg)
        response = {"message": "Données envoyés avec succès"}
        return jsonify(response), 200
    except Exception as e:
            response = {"error": str(e)}
            return jsonify(response), 400
          
    
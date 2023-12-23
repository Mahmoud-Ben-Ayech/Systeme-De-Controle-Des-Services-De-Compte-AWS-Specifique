import streamlit as st
from Parts import partEc2,partClf,partEcs,partLmbda,partRds,partS3,partVpc
from Home import BASE_URL,sendEmailNotification
import requests

url_users=BASE_URL+'/getUsers'
users_tab =requests.get(url_users).json()
users=[user for user in users_tab]

if "loggedinUser" not in st.session_state:
    st.session_state.loggedinUser=False


def login_user():
    st.title("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Sign in")

    if login_button:
        for user in users:
           if email == user["Email"]  and password ==user["Password"] :
               st.session_state.loggedinUser=True
               st.session_state.email=email
        if not st.session_state.loggedinUser :
            st.error("Check your details !")

def changePasswordUser():
    email=st.session_state.email
    old_password=st.text_input("Old Password",type="password")
    new_password=st.text_input("New Password",type="password")
    confirm_password=st.text_input("Confirm Password",type="password")
    update_button=st.button("Update")
    if update_button:
        if old_password and new_password and confirm_password :
          if new_password==confirm_password : 
            response=requests.post("http://localhost:5000/updatePasswordUser",json={"email":email,"oldPassword":old_password,"newPassword":new_password})
            if response.status_code==200:
                message=f"Your Password on Our Dashboard Platform AWS Account Has Been Changed to : \n Password :{new_password} "
                if sendEmailNotification(email,message):
                    st.success(f"Update Established & Mail sent to {email} !")
            else:
                st.error("Bad Credentiels !")
          else:
            st.error("Please ensure confirmation of new password !")      
        else:
            st.warning("Please fill in the fields !") 

def logoutFunction():
    if st.sidebar.button("logout"):
        st.session_state.loggedinUser=False

if not st.session_state.loggedinUser:
    login_user()
else : 
    match st.sidebar.radio("choix Utilisateur",["Partie Ec2","Partie S3","Partie RDS","Partie CloudFront","Partie Lambda"
                                    ,"Partie VPC","Partie ECS","Change Password"]) :
        case "Partie Ec2":
            logoutFunction()
            partEc2.afficher()
            partEc2.searchLoader()
        case "Partie S3" :
            logoutFunction()
            partS3.afficher()
            partS3.searchLoader()
            
        case "Partie RDS":
            logoutFunction()
            partRds.afficher()
            partRds.searchLoader()
            
        case  "Partie CloudFront":
            logoutFunction()
            partClf.afficher()
            partClf.searchLoader()
            
        case  "Partie Lambda":
            logoutFunction()
            partLmbda.afficher()
            partLmbda.searchLoader()
            
        case  "Partie VPC": 
            logoutFunction()  
            partVpc.afficher()
            partVpc.searchLoader()
                           
        case "Partie ECS":
            logoutFunction()
            partEcs.afficher() 
            partEcs.searchLoader()

        case "Change Password":
            logoutFunction()
            changePasswordUser()    
              
    
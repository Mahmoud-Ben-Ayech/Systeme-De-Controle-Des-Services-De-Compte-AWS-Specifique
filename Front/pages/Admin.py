import streamlit as st
from Parts import partEc2,partClf,partEcs,partLmbda,partRds,partS3,partVpc
import requests
from Home import BASE_URL,sendEmailNotification,verifier_email

url_users=BASE_URL+'/getUsers'
users_tab =requests.get(url_users).json()
users=[user["Email"] for user in users_tab]

url_admins=BASE_URL+'/getAdmins'
admins_tab=requests.get(url_admins).json()
admins=[admin for admin in admins_tab]


if "loggedinAdmin" not in st.session_state:
    st.session_state.loggedinAdmin=False

def manageUser():
    email=st.text_input("Email")
    password=st.text_input("Password",type="password")
    add_button=st.button("Add User")
    remove_button=st.button("Remove User")
    update_button=st.button("Update User")
    

    if add_button:
        if verifier_email(email) and password:
            response=requests.post("http://localhost:5000/addUser",json={"email":email,"password":password})
            if response.status_code==200:
                message=f"Your User Account has been successfully created in our AWS Account Dashboard application! \n With the following contact details : \n Email : {email} \n Password :{password} "
                if sendEmailNotification(email,message) :
                    st.success(f"Addition Established & Mail sent to {email} !")
                else :
                    st.error(f"Probleme in sending Email to {email} ! ")    
            else:
                st.error("Please check the email address !")
        else:
            st.warning("Incorrect email format or fields are not completed!")  

    if update_button:
        if verifier_email(email) and password:
            response=requests.post("http://localhost:5000/updateUser",json={"email":email,"password":password})
            if response.status_code==200:
                message=f"Your User Account has been Edit our AWS Account Dashboard Application With the Following Details : \n Email : {email} \n Password :{password} "
                if sendEmailNotification(email,message):
                    st.success(f"Update Established & Mail sent to {email} !")
                else :
                    st.error(f"Probleme in sending Email to {email} ! ")     
            else:
                st.error("Please check the Email address or no change detected!")
        else:
            st.warning("Incorrect email format or fields are not completed!")          

    if remove_button:
        if verifier_email(email) :
            response=requests.post("http://localhost:5000/removeUser",json={"email":email})
            if response.status_code==200:
                message=f"Your User Account has been Deleted from our AWS Account Dashboard application  "
                if sendEmailNotification(email,message):
                    st.success(f"Deletion Established & Mail sent to {email} !")
                else :
                    st.error(f"Probleme in sending Email to {email} ! ")     
            else:
                st.error("Please check the email address !")   
        else:
            st.warning("Incorrect email format or fields are not completed!")

def login_admin():
    st.title("Admin Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Sign in")
    if login_button:
        for admin in admins:
           if email == admin["Email"]  and password ==admin["Password"] :
               st.session_state.loggedinAdmin=True
               st.session_state.email=email
        if not st.session_state.loggedinAdmin :
            st.error("Check your details !")

def changePasswordAdmin():
    email=st.session_state.email
    old_password=st.text_input("Old Password",type="password")
    new_password=st.text_input("New Password",type="password")
    confirm_password=st.text_input("Confirm Password",type="password")
    update_button=st.button("Update")
    if update_button:
        if old_password and new_password and confirm_password :
          if new_password==confirm_password:  
            response=requests.post("http://localhost:5000/updatePasswordAdmin",json={"email":email,"oldPassword":old_password,"newPassword":new_password})
            if response.status_code==200:
                message=f"Your Password on Our Dashboard Platform AWS Account Has Been Changed to : \n Password :{new_password} "
                if sendEmailNotification(email,message):
                    st.success(f"Update Established & Mail sent to {email} !")
            else:
                st.error("Bad Credentiels  !")
          else:
            st.error("Please ensure confirmation of new password !")       
        else:
            st.warning("Please fill in the fields !")             

def logoutFunction():
    if st.sidebar.button("logout",key="narrow_button"):
        st.session_state.loggedinAdmin=False

if not st.session_state.loggedinAdmin:
    login_admin()
else : 
    match st.sidebar.radio("Admin choice",["Ec2 Part","S3 Part","RDS Part","CloudFront Part","Lambda Part"
                                    ,"VPC Part","ECS Part","Change Password","Manage Users"]) :
        case "Ec2 Part":     
            logoutFunction()
            partEc2.searchLoader()
            partEc2.afficher()
        case "S3 Part" :
            logoutFunction()
            partS3.searchLoader()
            partS3.afficher()
        case "RDS Part":
            logoutFunction()
            partRds.searchLoader()
            partRds.afficher()
        case  "CloudFront Part":
            logoutFunction()
            partClf.searchLoader()
            partClf.afficher()
        case  "Lambda Part":
            logoutFunction()
            partLmbda.searchLoader()
            partLmbda.afficher()
        case  "VPC Part": 
            logoutFunction()  
            partVpc.searchLoader()
            partVpc.afficher()               
        case "ECS Part":
            logoutFunction()
            partEcs.searchLoader()
            partEcs.afficher()  
        case "Change Password":
            logoutFunction()
            changePasswordAdmin() 
        case "Manage Users":
            logoutFunction() 
            st.markdown("<h3 style='color: #AD956B;'>Manage Users</h3>", unsafe_allow_html=True)   
            manageUser()
            st.markdown("<h3 style='color: #AD956B;'>List of Users</h3>", unsafe_allow_html=True) 
            st.table(users)
            
            
   
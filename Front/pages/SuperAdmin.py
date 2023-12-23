import streamlit as st
from Parts import partEc2,partClf,partEcs,partLmbda,partRds,partS3,partVpc
import requests
from Home import BASE_URL,email_super,pass_super,sendEmailNotification,verifier_email

url_users=BASE_URL+'/getUsers'
users_tab =requests.get(url_users).json()
users=[user["Email"] for user in users_tab]


url_admins=BASE_URL+'/getAdmins'
admins_tab=requests.get(url_admins).json()
admins=[admin['Email'] for admin in admins_tab]

if "loggedin" not in st.session_state:
    st.session_state.loggedin=False


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


def manageAdmin():
    email=st.text_input("Email")
    password=st.text_input("Password",type="password")
    add_button=st.button("Add Admin")
    remove_button=st.button("Remove Admin")
    update_button=st.button("Update Admin")
    

    if add_button:
        if verifier_email(email) and password:
            response=requests.post("http://localhost:5000/addAdmin",json={"email":email,"password":password})
            if response.status_code==200:
                message=f"Your Admin Account has been successfully created in our AWS Account Dashboard application! \n With the following contact details : \n Email : {email} \n Password :{password} "
                if sendEmailNotification(email,message):
                    st.success(f"Addition Established & Mail sent to {email} !")
                else :
                    st.error(f"Probleme in sending Email to {email} ! ")     
            else:
                st.error("Please check the email address !")
        else:
            st.warning("Incorrect email format or fields are not completed!")  

    if update_button:
        if verifier_email(email) and password:
            response=requests.post("http://localhost:5000/updateAdmin",json={"email":email,"password":password})
            if response.status_code==200:
                message=f"Your Admin Account has been Edit our AWS Account Dashboard Application With the Following Details : \n Email : {email} \n Password :{password} "
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
            response=requests.post("http://localhost:5000/removeAdmin",json={"email":email})
            if response.status_code==200:
                message=f"Your Admin Account has been Deleted from our AWS Account Dashboard application  "
                if sendEmailNotification(email,message):
                    st.success(f"Deletion Established & Mail sent to {email} !")
                else :
                    st.error(f"Probleme in sending Email to {email} ! ")     
            else:
                st.error("Please check the email address !")
        else:
            st.warning("Incorrect email format or fields are not completed!")



def login_superadmin():
    st.title("SuperAdmin Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Sign in")

    if login_button:
        if email == email_super and password ==pass_super:
            st.session_state.loggedin=True
        else:
            st.error("Check your details !")

def logoutFunction():
    if st.sidebar.button("logout",key="narrow_button"):
        st.session_state.loggedin=False

if not st.session_state.loggedin:
    login_superadmin()
else : 
    match st.sidebar.radio("SuperAdmin choice",["Ec2 Part","S3 Part","RDS Part","CloudFront Part","Lambda Part"
                                    ,"VPC Part","ECS Part","Manage Users","Manage Administrators"]) :
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
        case "Manage Users":
            logoutFunction() 
            st.markdown("<h3 style='color: #AD956B;'>Manage Users</h3>", unsafe_allow_html=True)   
            manageUser()
            st.markdown("<h3 style='color: #AD956B;'>List of Users</h3>", unsafe_allow_html=True) 
            st.table(users)
        case "Manage Administrators" :
            logoutFunction() 
            st.markdown("<h3 style='color: #AD956B;'>Manage Administrators</h3>", unsafe_allow_html=True)   
            manageAdmin()
            st.markdown("<h3 style='color: #AD956B;'>List of Administrators</h3>", unsafe_allow_html=True) 
            st.table(admins)   
            
            
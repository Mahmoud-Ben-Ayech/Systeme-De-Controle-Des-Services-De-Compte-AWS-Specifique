import streamlit as st
import datetime
import requests
import pandas as pd
import re
import boto3 
sns=boto3.client('sns')

#          ************* Header of Page  **************

st.set_page_config(page_title=" Dahboard AWS ")

#           **************  Recuperation de Flask  *********************

BASE_URL='http://localhost:5000'


#           **************  Paramtres de Configurations  ( à changer en cas de Besoins ) ***************** 

url_var_env=BASE_URL+'/varEnv'
temps_travail_Min=requests.get(f"{url_var_env}/getDebut").text
temps_travail_Max=requests.get(f"{url_var_env}/getFin").text
jours_travail=requests.get(f"{url_var_env}/getJours").json()
taille_bucket_max=requests.get(f"{url_var_env}/getTaille").json()

pass_super=requests.get(f"{url_var_env}/getPassSuper").text
email_super=requests.get(f"{url_var_env}/getEmailSuper").text


#          ***************  Functions For Notifications ERROR ***************

# Fonction d'envoi de Alert en cas d'erreur :
def sendMessage(ch):
    st.write (ch)
    """sns.publish(
            TopicArn='you_put_here_your_topicArn_to_recieve_the_notifications',  #you must put here your topicArn
            Message=ch
        )"""
    st.write('Notification sent Successfully !')


#            ****************  Variables Partagées  *******************


temps_actuelle=datetime.datetime.now().strftime("%H:%M:%S")
jour_actuelle=datetime.datetime.now().strftime("%A")
temps_Min=[int(e) for e in temps_travail_Min.split(':')]
temps_Max=[int(e) for e in temps_travail_Max.split(':')]
temps_Act=[int(e) for e in temps_actuelle.split(':')]


#           ***************  Fonctions Partagés  **********************

# Fonction qui verifie si on ait dans le periode de travail ou non :
def getConditionsTravail():
    cond_in_temps= temps_Min[0] <= temps_Act[0] <= (temps_Max[0]-1)
    cond_max_temps=temps_Act[0]==temps_Max[0] and 00  <= temps_Act[1] <= temps_Max[1]
    cond_min_temps= temps_Act[0]==temps_Min[0] and temps_Min[1] <= temps_Act[1] <= 60
    cond_jour_travail=jour_actuelle in jours_travail  
    
    cond_en_travail= (cond_in_temps or cond_max_temps or cond_min_temps) and cond_jour_travail
    return cond_en_travail

# Fonction qui va recuperer les donner selon la region choisit :
def recuperationData(d_table,name):
    list_regions_d=set(ins['REGION'] for ins in d_table)
    ch_d=st.selectbox(f"choose the region to consult the {name} : ",list_regions_d)
    if ch_d!='':
        st.write(f"<h4 style='color:#AD956B;'>For The Region : {ch_d}</h4>", unsafe_allow_html=True)
        d_reg=[ins for ins in d_table if ins['REGION']==ch_d]
    return d_reg

# Fonctions qui vont colrer le status  dans le tableaux':
def colorStatus(row,etat):
    if row == etat or row == 'stopped':
        return 'color: green'
    else:
        return 'color: red'

def stylingTab(tab_reg,etat):
    tab_reg_styled = pd.DataFrame(tab_reg) 
    regTab=tab_reg_styled.style.applymap(colorStatus, subset=['State'],etat=etat)
    return regTab

#Fonctions pour la Recherche : 

def searchData(url_data,choice_name,state_for_color):
    if st.button("Search"):
      try:
        response=requests.get(f"{url_data}/search/{choice_name}")
        if response.status_code==200 and response.json():
            result=response.json()
            if result:
                instance_tab=stylingTab(result,state_for_color)
                st.table(instance_tab)
        else:
            st.error(f"{choice_name} Not Found !")
      except requests.exceptions.RequestException as e:
        st.write(f"An error occurred: {e}")

def search_data_without_color_state(url_data,choice_name):
    if st.button("Search"):
      try:
        response=requests.get(f"{url_data}/search/{choice_name}")
        if response.status_code==200 and response.json():
            result=response.json()
            if result:
                st.table(result)
        else:
            st.error(f"{choice_name} Not Found !")
      except requests.exceptions.RequestException as e:
        st.write(f"An error occurred: {e}")

#Fonction pour envoyer les mails de creation des comptes Admin / User
def sendEmailNotification(email,message):
    response=requests.post("http://localhost:5000/send_email",json={"email":email,"message":message})
    if response.status_code==200:
        return True
    return False


#Fonction de verification de format des adresses Mails 
def verifier_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

#                       ***************  Main Home Page ***************

# Partie Presentation :
def PresentationApp():
    st.markdown("<h3 style='color: #AD956B;'>Application Overview</h3>", unsafe_allow_html=True)
    st.write("\n \n \n  Welcome to our AWS Account Application Dashboard.", 
             "In this application we have designed a simple interface to retrieve",
             " and visualize important data from your AWS account such as EC2 instances,",
             " ALBs and S3 buckets...")

# Partie EC2 :    
def partieEc2():
    st.markdown("<h4 style='color: #4AA3A2;text-align: center; '>EC2 Part</h4>", unsafe_allow_html=True)
    st.write("\n \n \n  In This Part We will see the following services: \n")
    st.write("* EC2 instances  \n * Load Balancers app \n * Elastic Block Storage  \n * Snapshots \n * Elastic IPs")
    st.image("./images/ec2.jpg")

# Partie VPC:
def partieVpc():  
    st.markdown("<h4 style='color: #4AA3A2;text-align: center; '>Virtual Private Cloud (VPC) part </h4>", unsafe_allow_html=True)
    st.write("\n \n \n  In This Part We will see the following services: \n")
    st.write("* Virtual Private Cloud   \n * Subnets \n *   Internet Getway  \n * Nat Getway \n * Vpc Endpoint")
    st.image("./images/vpc.jpg")  

# Partie ECS:
def partieEcs():
    st.markdown("<h4 style='color: #4AA3A2;text-align: center; '>Elastic Container Service (ECS) part</h4>", unsafe_allow_html=True)
    st.write("\n \n \n  In This Part We will see the following services: \n")
    st.write("* ECS Clusters  \n * ECS Task Definition \n ")
    st.image("./images/ecs.png")

# affichage des  differents parties du l'applications :
def partiesApp():    
    st.markdown("<h3 style='color: #AD956B;'>Parts of the Application</h3>", unsafe_allow_html=True)
    partieEc2()
    st.markdown("<h4 style='color: #4AA3A2;text-align: center; '>Buckets S3 part</h4>", unsafe_allow_html=True)
    st.image("./images/s3.png")

    st.markdown("<h4 style='color: #4AA3A2;text-align: center; '>Relational Database Service(RDS) part</h4>", unsafe_allow_html=True)
    st.image("./images/rds.png")

    st.markdown("<h4 style='color: #4AA3A2;text-align: center; '>Cloud Front Part</h4>", unsafe_allow_html=True)
    st.image("./images/clf.png")

    st.markdown("<h4 style='color: #4AA3A2;text-align: center; '>Lambda Functions Part </h4>", unsafe_allow_html=True)
    st.image("./images/lmb.png")

    partieVpc()
    partieEcs()
    


def main():
    st.markdown("<h1 style='color: #317AC1;text-align: center; '> Dashboard AWS Account </h1>", unsafe_allow_html=True)
    st.sidebar.success(" Choose the type of Connection to establish ") 
    PresentationApp()
    partiesApp()


if __name__ == '__main__':
    main()
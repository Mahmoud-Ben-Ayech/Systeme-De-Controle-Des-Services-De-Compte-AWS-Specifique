import streamlit as st
import requests
from Home import recuperationData,getConditionsTravail,sendMessage,search_data_without_color_state
from Home import BASE_URL
import pandas as pd


#                    *********  base_url de Partie  Rds  ******************** 

url_rds=BASE_URL+'/rds'


#                   ***********  Block for search *****************


def searchRds():
    st.markdown(f"<h3>Give  <span style='color:green;'> Rds Identifier  </span> to search</h3>", unsafe_allow_html=True)
    rds_name=st.text_input("")
    search_data_without_color_state(url_rds,rds_name) 
    



#                    *********  Partie RDS  ***************************


Rds_table=requests.get(f'{url_rds}/getAll').json()          #Recuperation tous les RDS

# Fonctions de Coloration de status  dans le  tableau :
def colorStatusRds(row):
    if row == 'available' or row == 'stopped':
        return 'color: green'
    else:
        return 'color: red'

def stylingTabRds(tab_reg):
    tab_reg_styled = pd.DataFrame(tab_reg) 
    regTab=tab_reg_styled.style.applymap(colorStatusRds, subset=['Status'])
    return regTab

# Fonctions de separation des Rds selon l'etat :
def remplissageTabRds(Rds_reg_table,cond_en_travail):
    Rds_normally,Rds_error,Rds_stopped=[],[],[]
    for rds in Rds_reg_table:
        if rds['Status']=='available' and cond_en_travail :
            Rds_normally.append(rds)
        elif rds['Status']=='available' and not cond_en_travail :    
            Rds_error.append(rds)
        elif rds['Status']!='available' :
            Rds_stopped.append(rds)
    return   Rds_normally,Rds_error,Rds_stopped

def getSeparedState(Rds_reg_table):
    cond_en_travail=getConditionsTravail()
    Rds_normally,Rds_error,Rds_stopped=remplissageTabRds(Rds_reg_table,cond_en_travail)
    return  Rds_normally,Rds_error,Rds_stopped
           
# Fonction de Notification En cas d'erreur :           
def NotifyErrorRds(rds_running_error):
    ch=""
    for rds in rds_running_error:
            ch+="* RDS "+rds['RDS Identifier']+" in region "+rds['REGION']+" is running Unexpectedly !! \n ****** \n"
    sendMessage(ch)

# Fonction d'affichage des Rds :
def affichageSeparedState(all_state_rds):
      if all_state_rds[0]:
        st.write(f"<h5 > Table of RDS  <span style='color:green;'>Running Normally: {len(all_state_rds[0])}  </span> Rds</h5>", unsafe_allow_html=True)
        st.table(all_state_rds[0])
      if all_state_rds[1]:  
        st.write(f"<h5 > Table of RDS  <span style='color:red;'>Running Error : {len(all_state_rds[1])} </span> Rds</h5>", unsafe_allow_html=True)
        st.table(all_state_rds[1])
        st.error('there are RDS unexpectedly run !', icon="🚨")
        button=st.button('Notify the team concerned')
        if button :
            NotifyErrorRds(all_state_rds[1]) 
      if all_state_rds[2]:
        st.write(f"<h5 >RDS Table <span style='color:green;'>Stopped :  {len(all_state_rds[2])}</span> Rds</h5>", unsafe_allow_html=True)
        st.table(all_state_rds[2])
      
def searchLoader():
    with st.sidebar:
        st.markdown(f"<h1 style='color: #317AC1;text-align: center;'>Particular Search</h1>", unsafe_allow_html=True)
        searchRds()
def afficher():
    # Partie Main pour RDS 

    st.markdown(f"<h3 style='color: #317AC1;'>RDS Information</h3>", unsafe_allow_html=True)
    Rds_reg_table=recuperationData(Rds_table,'RDS')
    affichageSeparedState(getSeparedState(Rds_reg_table))

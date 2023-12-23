import streamlit as st
import requests
from Home import recuperationData,sendMessage,search_data_without_color_state
from Home import BASE_URL,taille_bucket_max



#                    *********  base_url de partie S3  ******************** 

url_s3=BASE_URL+'/s3'


#                   ***********  Block for search *****************


def searchS3():
    st.markdown(f"<h3>Give  <span style='color:green;'> Bucket S3 Name </span> to search</h3>", unsafe_allow_html=True)
    s3_name=st.text_input("")
    search_data_without_color_state(url_s3,s3_name) 
    



#                    *********  Partie Buckets S3  ***************************


s3_table=requests.get(f'{url_s3}/getAll').json()     # Recuperation Tous les Buckets S3

# Fonction qui va separer les Buckets selon la taille :
def getSeparedState(s3_reg_table):
    s3_normally,s3_error=[],[]
    for buck in s3_reg_table:
        if float(buck['TailleMB']) <= float(taille_bucket_max) :
            s3_normally.append(buck)
        else :
            s3_error.append(buck)  
    return s3_normally,s3_error          

#Fonction qui va declancher l'appel de Notification en cas d'erreur :
def NotifyErrorBuckets(bucket_size_error):
    ch=""
    for buck in bucket_size_error:
            ch+="* bucket "+buck['Bucket Name']+" in region "+buck['REGION']+" is Over Size de taille :"+str(buck['TailleMB'])+" MB"+" !! \n ******\n "
    sendMessage(ch)

# Fonction d'affichage des Buckets separé : 
def affichageBucketSepared(all_state_buckets):
    if all_state_buckets[0]:
        st.write(f"<h5 > Table of Buckets S3 :  <span style='color:green;'> With Normal Size  : {len(all_state_buckets[0])} </span> Buckets</h5>", unsafe_allow_html=True)
        st.table(all_state_buckets[0])
    if  all_state_buckets[1] :   
        st.write(f"<h5 >Table of Buckets S3 :  <span style='color:red;'> Over Size   : {len(all_state_buckets[1])} </span> Buckets</h5>", unsafe_allow_html=True)
        st.table(all_state_buckets[1])
        st.error('there are Buckets with Over Size !', icon="🚨")
        button=st.button('Notify the team concerned')
        if button :
            NotifyErrorBuckets(all_state_buckets[1])  

def searchLoader():
    with st.sidebar:
        st.markdown(f"<h1 style='color: #317AC1;text-align: center;'>Particular Search</h1>", unsafe_allow_html=True)
        searchS3() 
def afficher():
    # Partie Main pour Bucket S3

    st.markdown(f"<h3 style='color: #317AC1;'>Buckets S3 Information</h3>", unsafe_allow_html=True)
    s3_reg_table=recuperationData(s3_table,'Buckets S3')
    affichageBucketSepared(getSeparedState(s3_reg_table))
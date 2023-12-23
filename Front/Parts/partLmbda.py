import streamlit as st
import requests
from Home import recuperationData,stylingTab,searchData
from Home import BASE_URL


#                    *********  base_url pour Lambda Functions  ******************** 


url_lambda=BASE_URL+'/lambda'


#                   ***********  Block for search *****************

def searchLmb():
    st.markdown(f"<h3>Give <span style='color:green;'> Lambda Function Name  </span>to search</h3>", unsafe_allow_html=True)
    lmb_name=st.text_input("")
    searchData(url_lambda,lmb_name,'Active') 
    


#                     ********* Partie Fonctions Lambda *******

Lmb_table=requests.get(f'{url_lambda}/getAll').json()    # Recuperation de Tous les Lambda functions 

def searchLoader():
     with st.sidebar:
        st.markdown(f"<h1 style='color: #317AC1;text-align: center;'>Recherche Particuliére</h1>", unsafe_allow_html=True)
        searchLmb()
def afficher():
   st.markdown(f"<h3 style='color: #317AC1;'>Lambda Functions Information</h3>", unsafe_allow_html=True)
   Lmb_reg=recuperationData(Lmb_table,'Lambda Functions')
   st.write('\n Lambda Functions Table: ',len(Lmb_reg),' fonctions ')
   lmbTab=stylingTab(Lmb_reg,'Active')
   st.table(lmbTab)
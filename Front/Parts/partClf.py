import streamlit as st
import requests
from Home import BASE_URL
from Home import stylingTab,searchData


#                    *********  base_url de partie Cloud Front   ******************** 

url_rds=BASE_URL+'/cloudfront'


#                   ***********  Block for search *****************


def searchClf():
    st.markdown(f"<h3> Give <span style='color:green;'> Cloud Front Alternate Domain </span> to search </h3>", unsafe_allow_html=True)
    rds_name=st.text_input("")
    searchData(url_rds,rds_name,'Deployed') 
    


#                     ********  Cloud Front **************

Clf_table=requests.get(f'{url_rds}/getAll').json()     # Recuperation de Tous les Cloud Front

def searchLoader():
     with st.sidebar:
        st.markdown(f"<h1 style='color: #317AC1;text-align: center;'> Particular Search</h1>", unsafe_allow_html=True)
        searchClf()
def afficher():
    st.markdown("<h3 style='color: #317AC1;'>CloudFronts Information </h3>", unsafe_allow_html=True)
    st.write('\n CloudFronts table : ',len(Clf_table),' Clf ')
    clfTab=stylingTab(Clf_table,'Deployed')
    st.table(clfTab)
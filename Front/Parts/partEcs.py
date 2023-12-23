import streamlit as st
from Home import recuperationData,search_data_without_color_state
from Home import BASE_URL
import pandas as pd
import requests

#                      *********  bases_urls pour la partie Ecs  ******************** 

url_ecs=BASE_URL+'/ecscluster'
url_task_def=BASE_URL+'/taskdef'




#                   ***********  Block for search *****************
def searchTaskDef():
    st.markdown(f"<h3>Give  <span style='color:green;'> Task Definition Name </span> to search</h3>", unsafe_allow_html=True)
    taskdef_name=st.text_input("Task Definition Name :")
    search_data_without_color_state(url_task_def,taskdef_name) 



#                      *********  Partie  ECS Clusters ******************** 

ecs_table=requests.get(f'{url_ecs}/getAll').json()  #Recuperation de tous les Ecs Clusters




#                      *********  Partie  Task Definitions ******************** 

tdef_table=requests.get(f'{url_task_def}/getAll').json()    #Recuperation de tous les Task Definitions


def colorStatusActive(row):
    if row == 'ACTIVE':
        return 'color: green'
    else:
        return 'color: red'

def stylingTabActive(tab_reg):
    tab_reg_styled = pd.DataFrame(tab_reg) 
    regTab=tab_reg_styled.style.applymap(colorStatusActive, subset=['Status Last Version'])
    return regTab

def searchLoader():
    with st.sidebar:
        st.markdown(f"<h1 style='color: #317AC1;text-align: center;'>Particular Search</h1>", unsafe_allow_html=True)
        searchTaskDef()


def afficher():

    st.markdown(f"<h3 style='color: #317AC1;'>ECS Clusters Information</h3>", unsafe_allow_html=True)
    ecs_reg=recuperationData(ecs_table,'ECS Clusters')
    st.write('\n ECS Table : ',len(ecs_reg),'ECS')
    st.table(ecs_reg)


    st.markdown(f"<h3 style='color: #317AC1;'>Task Definitions Information</h3>", unsafe_allow_html=True)
    tdef_reg=recuperationData(tdef_table,'Task Definitions')
    st.write('\n ECS Table : ',len(tdef_reg),'ECS')
    tdef_reg=stylingTabActive(tdef_reg)
    st.table(tdef_reg)
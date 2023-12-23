import streamlit as st
import requests
from Home import recuperationData,getConditionsTravail,sendMessage,stylingTab,searchData,search_data_without_color_state
from Home import BASE_URL


#                    *********  bases_urls pour la partie de Vpc  ******************** 

url_vpc=BASE_URL+'/vpc'
url_subnet=BASE_URL+'/subnet'
url_internet_getway=BASE_URL+'/internetgetway'
url_endpoint=BASE_URL+'/vpcendpoint'
url_nat_getway=BASE_URL+'/natgetway'


#                    ******** Block for search functions **********************


def searchVpc():
    st.markdown(f"<h3>Give <span style='color:green;'> Vpc State </span> to search</h3>", unsafe_allow_html=True)
    vpc_name=st.selectbox("",["available", "other"])
    searchData(url_vpc,vpc_name,"available")
    
def searchSubnet():
    st.markdown(f"<h3>Give<span style='color:green;'> Subnet State </span>to search</h3>", unsafe_allow_html=True)
    subnet_name=st.selectbox("",["available", "other"])
    searchData(url_subnet,subnet_name,"available")

def searchIgetway():
    st.markdown(f"<h3>Give<span style='color:green;'> Internet Getway State </span> to search</h3>", unsafe_allow_html=True)
    igtw_name=st.selectbox("",["available", "other"])
    searchData(url_internet_getway,igtw_name,"available")

def searchNgetway():
    st.markdown(f"<h3>Give<span style='color:green;'> Nat Getway State </span>to search</h3>", unsafe_allow_html=True)
    ngtw_name=st.selectbox("",["available", "other"])
    search_data_without_color_state(url_nat_getway,ngtw_name)

def searchEndpoint():
    st.markdown(f"<h3>Give <span style='color:green;'> Vpc Endpoint Name </span>to search</h3>", unsafe_allow_html=True)
    endpoint_state=st.text_input("Vpc Endpoint Name :")
    searchData(url_endpoint,endpoint_state,"available")
                              

#                    *********  Partie Nat Getway  ******************** 

ngw_table=requests.get(f'{url_nat_getway}/getAll').json()       #Recuperation de tous les NatGetways

# Fonction de separation de NatGetways selon l'etat :
def getSeparedState(ngw_reg_table):
    ngw_normally,ngw_error=[],[]
    cond_en_travail=getConditionsTravail()
    for ngw in ngw_reg_table:
            if ngw['State']=='available' and cond_en_travail :
                ngw_normally.append(ngw)
            elif ngw['State']=='available' and not cond_en_travail :
                ngw_error.append(ngw) 
    return  ngw_normally,ngw_error  

# Fonction de Notification En cas d'erreur : 
def NotifyErrorNatgetway(natgetway_creation__error):
    ch=""
    for ngw in natgetway_creation__error:
            ch+="* Nat Getway "+ngw['Name']+" with Id "+ngw['Nat Getway Id']+" in region"+ngw['REGION']+" is created Unexpectedly !! \n ****** \n"
    sendMessage(ch)

# Fonction d'affichage des NatGetways : 
def affichageSeparedState(all_state_vpc):
    if all_state_vpc[0] :
        st.write(f"<h5 >Table of Nat Getways  <span style='color:green;'> Normally Created : {len(all_state_vpc[0])} </span> NGWay</h5>", unsafe_allow_html=True)
        st.table(all_state_vpc[0])
    if all_state_vpc[1]:
        st.write(f"<h5 >Table of Nat Getways  <span style='color:red;'>  Unexpectedly Created : {len(all_state_vpc[1])} </span> NGWay</h5>", unsafe_allow_html=True)
        st.table(all_state_vpc[1])
        st.error('there are NatGetway unexpectedly created !', icon="🚨")
        button=st.button('Notify the team concerned')
        if button :
            NotifyErrorNatgetway(all_state_vpc[1]) 


def searchLoader():
     with st.sidebar:
        st.markdown(f"<h1 style='color: #317AC1;text-align: center;'> Particular Search </h1>", unsafe_allow_html=True)
        match st.selectbox(" Select service to search ", ["Vpc", "Subnet", "Internet Getway", "Nat Getway","Vpc Endpoint"]) :
            case "Vpc": 
                searchVpc()
            case  "Subnet":   
                searchSubnet()  
            case "Internet Getway": 
                searchIgetway()  
            case "Nat Getway": 
                searchNgetway()  
            case "Vpc Endpoint": 
                searchEndpoint()  

def afficher() :
     #                      *********  Partie  VPCs ******************** 

    vpc_table=requests.get(f'{url_vpc}/getAll').json()  #Recuperation de tous les Vpcs

    st.markdown(f"<h3 style='color: #317AC1;'> VPCs Information</h3>", unsafe_allow_html=True)
    vpc_reg=recuperationData(vpc_table,'VPCS')
    st.write('\n VPCs Table : ',len(vpc_reg),'VPC')
    vpc_reg=stylingTab(vpc_reg,'available')
    st.table(vpc_reg)

    #                      *********  Partie Subnets  ******************** 

    sub_table=requests.get(f'{url_subnet}/getAll').json()    #Recuperation de tous les Subnets

    st.markdown(f"<h3 style='color: #317AC1;'>Subnets Information</h3>", unsafe_allow_html=True)
    sub_reg=recuperationData(sub_table,'Subnets')
    st.write('\n Subnets Table  : ',len(sub_reg),'Subnet')
    sub_reg=stylingTab(sub_reg,'available')
    st.table(sub_reg)

    #                    *********  Partie Internet Getway  ******************** 

    igw_table=requests.get(f'{url_internet_getway}/getAll').json()     #Recuperation de tous les Internet Getways

    st.markdown(f"<h3 style='color: #317AC1;'>Internet Getways Information</h3>", unsafe_allow_html=True)
    igw_reg=recuperationData(igw_table,'Internet Getways')
    st.write('\n Internet Getways Table: ',len(igw_reg),'IGWay')
    igw_reg=stylingTab(igw_reg,'available')
    st.table(igw_reg)

    # Partie Main pour Nat Getways

    st.markdown(f"<h3 style='color: #317AC1;'>Nat Getways Information</h3>", unsafe_allow_html=True)
    ngw_reg_table=recuperationData(ngw_table,'Nat Getways')
    affichageSeparedState(getSeparedState(ngw_reg_table))


    #                    *********  Partie VPC Endpoint  ******************** 

    vpce_table=requests.get(f'{url_endpoint}/getAll').json()     #Recuperation de tous les Endpoint



    st.markdown(f"<h3 style='color: #317AC1;'>Vpc Endpoint Information</h3>", unsafe_allow_html=True)
    vpce_reg=recuperationData(vpce_table,'Vpc Endpoint')
    st.write('\n Vpc Endpoint Table: ',len(vpce_reg),'VPCE')
    vpce_reg=stylingTab(vpce_reg,'available')
    st.table(vpce_reg)
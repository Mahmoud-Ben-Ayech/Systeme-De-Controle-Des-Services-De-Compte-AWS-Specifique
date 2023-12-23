import streamlit as st
import requests
from Home import recuperationData,getConditionsTravail,sendMessage,stylingTab,searchData,search_data_without_color_state
from Home import BASE_URL


#                    *********  base_Url des Parties   ******************** 

url_instances=BASE_URL+'/ec2'
url_alb=BASE_URL+'/alb'
url_ami=BASE_URL+'/ami'
url_ebs=BASE_URL+'/ebs'
url_snapshot=BASE_URL+'/snapshot'
url_elasticip=BASE_URL+'/eip'


#                    ******** Block for search functions **********************


def searchInstance():
    st.markdown(f"<h3>Give  <span style='color:green;'> Instance Name  </span> to search</h3>", unsafe_allow_html=True)
    instance_name=st.text_input("Instance Name :")
    searchData(url_instances,instance_name,"running")
    
def searchAlb():
    st.markdown(f"<h3>Give <span style='color:green;'> Alb Name </span> to search</h3>", unsafe_allow_html=True)
    alb_name=st.text_input("Alb Name :")
    searchData(url_alb,alb_name,"active")

def searchAmi():
    st.markdown(f"<h3>Give <span style='color:green;'> Ami Name </span> to search</h3>", unsafe_allow_html=True)
    ami_name=st.text_input("Ami Name :")
    searchData(url_ami,ami_name,"available")

def searchEbs():
    st.markdown(f"<h3>Give <span style='color:green;'> Ebs Name </span> to search</h3>", unsafe_allow_html=True)
    ebs_name=st.text_input("Ebs Name :")
    searchData(url_ebs,ebs_name,'available')

def searchSnapshot():
    st.markdown(f"<h3>Donner l'<span style='color:green;'> State of Snapshot </span> to search</h3>", unsafe_allow_html=True)
    snap_state=st.selectbox("",["completed", "other"])
    searchData(url_snapshot,snap_state,"completed")

def searchEip():
    st.markdown(f"<h3>Give <span style='color:green;'>Elastic Ip Name </span> to search</h3>", unsafe_allow_html=True)
    eip_name=st.text_input("Elastic Ip Name :")
    search_data_without_color_state(url_elasticip,eip_name)                                


               


#                   **********  Partie Instances EC2  **********************


ec2_table=requests.get(f'{url_instances}/getAll').json()    # Recuperation de tous les Instances  

# Fonctions Qui Vont separer  les instances selon l'etat :
def remplissageTabInstances(instances_reg):
    ec2_running_normally,ec2_running_error,ec2_other=[],[],[]
    cond_en_travail=getConditionsTravail()
    for instance in instances_reg:
        cond_stat=instance['State']=='running'
        if cond_stat and cond_en_travail:
            ec2_running_normally.append(instance)
        elif  cond_stat and not cond_en_travail :
            ec2_running_error.append(instance)  
        elif   not cond_stat  :
            ec2_other.append(instance) 
    return  ec2_running_normally,ec2_running_error,ec2_other       

def getInstancesSepared(instances_reg):
    ec2_running_normally,ec2_running_error,ec2_other=remplissageTabInstances(instances_reg)    
    return  ec2_running_normally,ec2_running_error,ec2_other  


# Fonction d'appel de Notification en cas d'erreur:
def NotifyErrorInstances(instances_running_error):
    ch=""
    for instance in instances_running_error:
            ch+="* instance "+instance['Instance Name']+" with id  "+instance['instance ID']+" in region "+instance['REGION']+" is running Unexpectedly !! \n ******** \n"
    sendMessage(ch)


# Fonction d'affichage des instances Separé selon l'etat :
def affichageInstancesSepared(all_state_instances) :
    if all_state_instances[0] :
        st.write(f"<h5 >Instances EC2 <span style='color:green;'>Running Normally: {len(all_state_instances[0])} </span> Instances</h5>", unsafe_allow_html=True)
        st.table(all_state_instances[0])
    if all_state_instances[1]:    
        st.write(f"<h5 >Instances EC2 <span style='color:red;'>Running Error: {len(all_state_instances[1])} </span> Instances</h5>", unsafe_allow_html=True)
        st.table(all_state_instances[1])
        st.error('there are instances unexpectedly run', icon="🚨")
        button=st.button('Notify the team concerned')
        if button :
            NotifyErrorInstances(all_state_instances[1])        
    if all_state_instances[2]:    
        st.write(f"<h5 >Instances EC2 <span style='color:green;'>stopped and terminated  : {len(all_state_instances[2])} </span> Instances</h5>", unsafe_allow_html=True)
        st.table(all_state_instances[2])

def searchLoader():
    with st.sidebar:
        st.markdown(f"<h1 style='color: #317AC1;text-align: center;'>Particular Search</h1>", unsafe_allow_html=True)
        match st.selectbox(" Select Service to search ", ["Instance Ec2", "Alb", "Ami", "Ebs","Snapshot","Elastic Ip"]) :
            case "Instance Ec2": 
                searchInstance()
            case  "Alb":   
                searchAlb()  
            case "Ami": 
                searchAmi()  
            case "Ebs": 
                searchEbs()  
            case "Snapshot": 
                searchSnapshot()  
            case "Elastic Ip": 
                searchEip() 


def afficher():

    # Partie Main pour Instances Ec2

    st.markdown(f"<h3 style='color: #317AC1;'>Ec2 Instances Information</h3>", unsafe_allow_html=True)
    instances_reg=recuperationData(ec2_table,'Instances Ec2')
    affichageInstancesSepared(getInstancesSepared(instances_reg))


    #                *************  Partie ALBs  ****************************

    alb_table=requests.get(f'{url_alb}/getAll').json()    # Recuperation de tous les Albs  

    st.markdown(f"<h3 style='color: #317AC1;'>ALBs Information</h3>", unsafe_allow_html=True)
    alb_reg=recuperationData(alb_table,'ALBs')
    st.write('\n Alb Table : ',len(alb_reg),'Albs')
    alb_reg=stylingTab(alb_reg,'active')
    st.table(alb_reg)

    #                 *************  Partie AMIs  ****************************

    ami_table=requests.get(f'{url_ami}/getAll').json()    # Recuperation de tous les Amis  

    st.markdown(f"<h3 style='color: #317AC1;'> AMIs Information</h3>", unsafe_allow_html=True)
    ami_reg=recuperationData(ami_table,'AMIs')
    st.write('\n AMI Table : ',len(ami_reg),'AMIs') 
    ami_reg=stylingTab(ami_reg,'available')
    st.table(ami_reg)

    #                *************  Partie EBSs  ****************************

    ebs_table=requests.get(f'{url_ebs}/getAll').json()       # Recuperation de tous les Ebs  

    st.markdown(f"<h3 style='color: #317AC1;'>EBSs Information</h3>", unsafe_allow_html=True)
    ebs_reg=recuperationData(ebs_table,'EBSs')
    st.write('\n EBS Table : ',len(ebs_reg),'EBS')
    ebs_reg=stylingTab(ebs_reg,'available')
    st.table(ebs_reg)

    #                *************  Partie SNAPSHOTS  ****************************

    snap_table=requests.get(f'{url_snapshot}/getAll').json()       # Recuperation de tous les Snapshots  

    st.markdown(f"<h3 style='color: #317AC1;'>Snapshots Informations</h3>", unsafe_allow_html=True)
    snap_reg=recuperationData(snap_table,'Snapshots')
    st.write('\n SNAPSHOT Table  : ',len(snap_reg),'SNAPSHOT')
    snap_reg=stylingTab(snap_reg,'completed')
    st.table(snap_reg)


    #                *************  Partie Elastic Ips  ****************************

    eip_table=requests.get(f'{url_elasticip}/getAll').json()        # Recuperation de tous les Elastic Ips  

    st.markdown(f"<h3 style='color: #317AC1;'>IElastic IPs Information</h3>", unsafe_allow_html=True)
    eip_reg=recuperationData(eip_table,'Elastic IPs')
    st.write('\n ELASTIC IP Table : ',len(eip_reg),'EIP')
    st.table(eip_reg)
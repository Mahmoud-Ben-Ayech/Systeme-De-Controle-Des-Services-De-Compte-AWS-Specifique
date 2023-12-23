# AWS Specific Account Services Control System

This project consist of management of services used by an AWS account and facilitate the access to resources and statistics without the need to AWS interface.

# Running Details 

As a first step of running you have to launch recuperation  script by this command "python3 selectData.py"  and also ***mongoDb server*** must be activated. 

---

And you must set some environment variables before launching the backend server which is : 

***SENDER_EMAIL*** , ***APP_PASSWORD***  => Information of mail to send the notification of the creation account of users.

***NAME_DATABASE*** , ***TEMPS_DEBUT*** , ***TEMPS_FIN*** , ***JOURS_TRAVAIL*** ,***TAILLE_BUCKET_MAX*** => informations needs for working time of Campany. 

***SUPER_EMAIL*** , ***SUPER_PASSWORD***  => Informations of mail of ***superuser*** of application who's permitted to create users and admins for app.

## Example of exportation variable :

 >> export TEMPS_DEBUT=08:00:00

 >> export JOURS_TRAVAIL= Monday, Tuesday, Wednesday, Thursday, Friday

---

Next, you need to launch backend  side ***Flask Framework*** by this command "python3 run.py" .

Finally you must launch Frontend Side ***Streamlit Framework*** by this command  "streamlit run Home.py"  

# Application Interfaces 

After the running of the project, this interface will be shown to allow you to login with SUPER_EMAIL and SUPER_PASSWORD that you passed as environment variables :

![login3](https://github.com/Mahmoud-Ben-Ayech/Systeme-De-Controle-Des-Services-De-Compte-AWS-Specifique/assets/104568399/af223c87-e4ef-4e1f-9bf2-000def71a5cc)




                                  


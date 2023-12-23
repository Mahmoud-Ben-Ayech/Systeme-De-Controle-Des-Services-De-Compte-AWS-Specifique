# AWS Specific Account Services Control System

This project consist of management of services used by an AWS account and facilitate the access to resources and statistics without the need to AWS interface.

# Running Details 

As a first step of running you have to launch recuperation  script by this command "python3 selectData.py"  and also ***mongoDb server*** must be activated. 

---

And you must set an environment variable before launching the backend server which is : 

***SENDER_EMAIL*** , ***APP_PASSWORD***  => Information of mail to send the notification of the creation account of users.

***NAME_DATABASE*** , ***TEMPS_DEBUT*** , ***TEMPS_FIN*** , ***JOURS_TRAVAIL*** ,***TAILLE_BUCKET_MAX*** => informations needs for working time of Campany. 

***SUPER_EMAIL*** , ***SUPER_PASSWORD***  => Informations of mail of ***superuser*** of application who's permitted to create users and admins for app.

## Example of exportation variable :

 >> export TEMPS_DEBUT=08:00:00

 >> export JOURS_TRAVAIL= Monday, Tuesday, Wednesday, Thursday, Friday

---

Next, you need to launch backend  side ***Flask Framework*** by this command "python3 run.py" .

Finally you must launch Frontend Side ***Streamlit Framework*** by this command  "streamlit run Home.py"  


                                  


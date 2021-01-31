
# covid-policy-tracker
RMIT cloud computing 

### Designed and Developed by : Vaishali Wahi | Yanying Xu
#### Appplication Link :http://flask-env.eba-au6i98zk.ap-southeast-2.elasticbeanstalk.com

## Introduction
As cited on the UpToDate website: ‘Coronaviruses are important human and animal pathogens. At the end of 2019, a novel coronavirus was identified as the cause of a cluster of pneumonia cases in Wuhan, a city in the Hubei Province of China. It rapidly spread, resulting in an epidemic throughout China, followed by a global pandemic. In February 2020, the World Health Organization designated the disease COVID-19, which stands for coronavirus disease 2019. The virus that causes COVID-19 is designated severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2); previously, it was referred to as 2019-nCoV’. (McIntosh 2020, para 1) 

While this virus has infected nearly a hundred people and claimed over 2 millions lives around the world at the time of writing this report, governments from all around the world have set up different policies during different stages of the pandemic to protect their citizens. While these public health policies have served the purpose of protecting the health of the citizens, it is recognized that they can have different effectiveness. Since many of these policies or restrictions have greatly impacted our daily lives since last year, we decided to develop a web app to track them. Hopefully from the current data we have collected, we can find some close answers to the most effective policies. 

We would like to point out, in this project, the policy data we used is sourced from the Oxford Coronavirus Government Response Tracker (OxCGRT).The Oxford COVID-19 Government Response Tracker (OxCGRT) systematically tracks and records information on different common policy responses that the governments had implemented to response to the pandemic on 18 indicators such as school closures and travel restrictions. We have selected 3 data sets for our current project. (University of Oxford, 2020) The covid cases data we are sourced from the Johns Hopkins University's coronavirus dataset. (Johns Hopkins University of Medicine 2020) All data we sourced can be found  in the Google BigQuery public dataset.

## High Level Architecture
![architecture](https://user-images.githubusercontent.com/55371863/106376056-a3b2d980-63e5-11eb-8565-ca46b6ce903c.png)

## Developer Guide


- Login Into EC2 Instance
  - To install navigate to https://aws.amazon.com/getting-started/tutorials/deploy-code-vm/
- Clone the git repository
- Install python 3.6 on the choosen OS in AWS
  To install navigate to https://phoenixnap.com/kb/how-to-install-python-3-ubuntu
- Install pip
  To install navigate to https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/
- Install virtual Environment
```
$ pip install virtualenv
```
- Create virtual Environment
```
$  virtualenv virt
```
- Activate virtual environment
```
$ virt/bin/activate
```
- _Now Install All the required Dependencies for the Project
- Install Flask
```
$ pip install flask
```
- To Fetch Data, create new lamda functions in AWS Lambda.(You can find the code in Lambda folder)
- Create API Gateway to use the lambda functions 
- Set Up Google cloud Project and enable Google Big Query
  To Learn how navigate to https://cloud.google.com/resource-manager/docs/creating-managing-project
- Create a CRON Job in EC2 instance to fed the data in real Time
  Set Up the following




### To run the application in local host
```
$ python application.py
```

### To run the application on server
- Deply the application on elstic beanstalk



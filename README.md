# Fog & Cloud Computing project 

by Matteo Caliandro, <matteo.caliandro@studenti.unitn.it>, <mcaliandro92@gmail.com>  
Lab Project for Fog & Cloud Computing course @ University of Trento - Italy  

**GitHub repo**: https://github.com/mcaliandro/fogcloud-project.git  


## Contents
1. [Introduction to SmartHomeSystem](#1-introduction-to-smarthomesystem)  
2. [Version Deployments](#2-version-deployments)  
3. [Why PaaS](#3-why-paas)


## 1. Introduction to SmartHomeSystem
The application is a prototype of a (simplified) remote monitoring service for a smart home system (SHS), where users (house owners) can access, from the outside, the smart home system placed at their own house in order to monitor and modify the status of the system in real time.

### 1.1. Datastore 
A database in which all the information about the SHS is stored. More specifically, it is a stand-alone service that hosts a [Mongo](https://www.mongodb.com/) database. The only entity in charge to interact with it is the Core Stack, which implements a proper interface to the MongoDB system.

### 1.2. Core 
A back-end application, written from the scratch in Python and developed by using [Flask](https://palletsprojects.com/p/flask/) framework and [Flask RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) extension, that exposes REST APIs for exchanging data between the SHS and the house owners. It is directly connected to a data store in order to persist the information sent by the remote system and to retrieve it when users ask for it.

### 1.3 Dashboard 
A front-end application that shows a dashboard in which users (house owners) can access the information provided by the SHS. The application is developed in Python by using Flask.

### 1.4. Smart Home System Emulation
The application doesn't rely on any specific implementation of a SHS, so it has been assumed that a device connected to the Internet, such as a Raspberry Pi, collects information about the SHS status in real time and sends it to the application. For this reason, the platform exposes APIs, so that the interaction with multiple devices can be emulated by using a Python script ([shs-simulator](https://github.com/mcaliandro/fogcloud-project/tree/master/utils/shs-emulator)) that periodically sends HTTP's PUT requests to the platform, containing the data about the (supposed) updated status of the SHS. This script is used to test the performance of the application under high workload too.

### 1.5. House Owner Emulation
To test the performance of the application on the PaaS, a Python script ([ho-simulator](https://github.com/mcaliandro/fogcloud-project/tree/master/utils/ho-emulator)) is used to periodically send HTTP's GET requests for retrieving the updated status of the SHS to the platform.

## 2. Version Deployments

### 2.1. Datastore
Once the datastore is deployed, it will run for the entire application's lifecycle, without being affected by subsequent version deployments of the application. The datastore is initialized through a Python script ([initdb](https://github.com/mcaliandro/fogcloud-project/tree/master/utils/initdb)) that populates it by performing HTTP requests to Core.

### 2.2. Version 1
**Core** ([source](https://github.com/mcaliandro/fogcloud-project/tree/master/application/core/v1))  
The back-end exposes the interfaces useful to allow the interaction with Dashboard and the SHS emulator. Briefly, the APIs provide the resources *User* and *SHS*. The APIs allows the GET method on */user/id*, GET and PUT methods are accepted on */shs/id*.

**Dashboard** ([source](https://github.com/mcaliandro/fogcloud-project/tree/master/application/dashboard/v1))  
The front-end is developed in Python and Flask to perform GET requests to Core and to show the information about a SHS on a plain HTML page.

### 2.3. Version 2
**Core** ([source](https://github.com/mcaliandro/fogcloud-project/tree/master/application/core-stack/v2))  
In this version, the back-end APIs replace the resource *User* with *Login* that allow Dashboard to perform the login of the user by using GET */login*. Instead, GET */shs/id* and PUT */shs/id* operations on the resource *SHS* are still accepted.

**Dashboard** 
The front-end keeps the vesion 1 which doesn't work with the new version of Core because it doesn't implement the new changes required by the back-end, like the user authentication to the platform.

## 3. Why PaaS

### 3.1. Application Requirements
**Datastore Stack**  
The application consists of a single instance of a Mongo database, that must always be available and reachable by Core. Furtermore, the database content must be stored into a peristent volume in order to avoid loss of data due the possible single instance failures.

**Core Stack**  
The application consists of multiple back-end instances aimed to provide the APIs to SHS devices and Dashboard. For this reason, it must be exposed to the external world to guarantee such a service and be scaled up/down according to the required workload. Furthermore, the stack will be subject to continuous updates, so new version deployments and related rollback operations are considered important.

**Dashboard Stack**  
The application consists of multiple front-end instances accessible by end users via web browser. This stack shares the same requirements of the Core stack: it must be exposed to the external world, be scaled up/down according to the number of connected users and be subject to frequent new version deployments and eventual deployment rollbacks.

### 3.2. Containerization and Ochestration
This project consists of deploying an application, with a set of specified requirementes, on a PaaS so that it can be easily extended with new features and be scaled. Docker, as containerization technology tool, allows the packaging of this application into standardized units [[cit](https://www.docker.com/resources/what-container)], called containers, which are automatically deployed, orchestrated, managed and scaled by Kubernetes [[cit](https://kubernetes.io/)]. For testing purposes, the project is hosted into a Linux virtual machine. This local environment doesn't provide a physical distributed infrastructure and such a distributed fashion should be emulated with a proper methodology. Here, a tool called [Kind](https://kind.sigs.k8s.io/) is used to create a single-node/multi-nodes Kubernetes cluster in a Docker environment where containers managed by Kind act as Kubernetes nodes. The scope is to create a multi-nodes cluster in which the application components (stacks) can be containerized and then orchestrated.

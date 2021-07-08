# Escape-traffic

**Team members**

* Mohammad Nada

* Abdel Hadi Nofal

* Qusai Qishta

* Abdalrahman Samara

### **Traffic Percentage**

Our idea is to count the cars going on a certain street, and return a live percentage of the traffic jam. If the percentage reaches a certain point, it will send an alarm. also, if there is a human life in danger on highways, we will contact the athorities directly to tell them that there is a possibility of an accident on that road, and they need to check the cameras.

This project would save people from getting stuck in a traffic jam, and it would save lives

### **PM**

for the project management, we are going to use Trello, to divide all the tasks and focus on the workflow of the project

[Our Project Management Tool](https://trello.com/b/Cdz722Xv/team-project)

### User Stories: 
 

1. Webcam or video ; As a user I want my application to open my cam.
    a.Feature Task:
         I can Choice my cam, or upload the video from my side
    b. Acceptance Test :
            insure can I add the video to test.
2. Count; As a user I want to count the cars in the street .
    a. Feature Tasks:
        the app count all cars in the screen and give the result
    b. Acceptance Test :
	    return the all counted cars , as number 
3. HighAccuracy; As a user I want high accuracy to count cars.
    a. Feature Tasks:
        most the accuracy more than 90% 
    b. Acceptance Test 
        test by img , already known the counts number , 
        test the video that have result a;ready
4. Get percentage; As A user I want to get the percentage of cars in
   a. Feature Tasks: 
        a. depends on the street, I want to know how much traffic is ?as result  
    b. Acceptance Test 
        test the known street capacity and 
5. Text Alarm; As a User I want to send me A text that tell me there A high traffic in
   a. Feature Tasks: 
        in case the street have 90% or more then The app will send a text to relative department to inform 
    b. Acceptance Test 
        add number text it manually 

## Installation

there are two installations, for people who have nvedia External graphics cards and for the ones who don't, the first one is for the one's who don't have the card, they must use it, and it's optional for people who have the card to choose between the first and the second one:

> first way for installation (Recommended)

you **must** use this installation if you **don't have nvedia External graphics card**, i will walk you through each step:

1. clone this repository on your local machine.

2. install Anaconda : press on this link [here](https://www.anaconda.com/products/individual) to install anaconda

3. after finishing installing Anaconda, Enter the Application, the enterface below is what are you going to see, select CMD.exe Prompt Launcher as in the image:

![image](./resources/1.PNG)

4. now, we need to create the Environment to hold all the libraries, most of the libraries will be installed automatically, but you need to add some of them by yourself. to create an environment and download dependencies, you need to Enter this command inside the CMD:

this command is for Tenserflow GPU, if you want to run the code on your GPU, which is way faster than the CPU:

``` conda env create -f project.yml ```

and this code is for Tenserflow CPU:

``` conda env create -f project1.yml ```

this command will create the environment for you, this will take some time

5. every time you need to work on the repository, you need to activate the environment. to activate the Environment, Enter this command:

``` conda activate project ```

currently, you are inside the environment.

6. there is one folder (the weights folder), that you need to install from google drive, this folder could not be pushed to github because it's extremely large, click on this [Link](https://drive.google.com/drive/folders/14NaJincTk836Buun76YlgmAIGFV69Ubx?usp=sharing) to download the checkpoints folder, after you download it, you need put directly inside the repository's folder.

7. type ``` python a.py ``` to run the GUI for this project

> second way for installation

if you have nvedia External graphics card, there is no need to do the first installation. instead, you can follow these steps:

1. clone this repository on your local machine.

2. now, we need to install all the libraries, most of the libraries will be installed automatically, but you need to add some of them by yourself. to create an environment and download dependencies, you need to Enter this command inside the CMD:

for Tenserflow on CPU:

``` pip install -r requirements.txt ```

for Tenserflow on GPU:

``` pip install -r requirements-gpu.txt ```

## Nvidia Driver (For GPU, if you are not using Conda Environment and haven't set up CUDA yet)

Make sure to use CUDA Toolkit version 10.1 as it is the proper version for the TensorFlow version used in this repository.

you can install it directly from [here](https://developer.nvidia.com/cuda-10.1-download-archive-update2)

3. there is one folder (the weights folder), that you need to install from google drive, this folder could not be pushed to github because it's extremely large, click on this [Link](https://drive.google.com/drive/folders/14NaJincTk836Buun76YlgmAIGFV69Ubx?usp=sharing) to download the checkpoints folder, after you download it, you need put directly inside the repository's folder.

4. type ``` python a.py ``` to run the GUI for this project

## IMPORTANT NOTES:

* some of the dependencies might not be installed, you just need to install them using:

``` pip install (name of the library) ```

* if you want to have the same experience with the phone calls, you need to register on [this](https://twilio.com/) website, get the account sid, auth token and the phone number, then replace them inside detect_video.py with your own, don't forget to validate you phone number and replace the one that is there right now.

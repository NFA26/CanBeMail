# CanBeMail

In an era where digital communication plays a pivotal role in our daily lives, the need for secure and private email communication is more critical than ever. *CanBeMail* is a Python-based desktop application designed to address this growing concern by providing users with a robust and user-friendly platform for sending and receiving encrypted emails through the widely-used Gmail service.

## Create User Password

Since the Gmail service does not allow using real Gmail account passwords, **you should generate an app password to use the CanBeMail app**.


### Step1: Click on *Manage Your Google Account*.

![image](https://github.com/NFA26/CanBeMail/assets/134808112/d9ab3bf1-948a-469d-9a59-17b33cc8b662)



### Step2: Navigate to the *Security* section.

<img width="233" alt="image" src="https://github.com/NFA26/CanBeMail/assets/134808112/9b5321b5-db2b-4635-a1f8-cbb2ab0e4d10">



### Step3: Scroll down and Click on *2-Step Verification*.

<img width="623" alt="image" src="https://github.com/NFA26/CanBeMail/assets/134808112/59fe14c9-74c3-4015-b560-8d7559063fdc">



### Step4: Turn on *2-Step Verification*.

<img width="280" alt="image" src="https://github.com/NFA26/CanBeMail/assets/134808112/a11d092c-4b8f-4043-8af1-bde101fe6866">



### Step5: Scroll down and Click on *App passwords* section.

<img width="619" alt="image" src="https://github.com/NFA26/CanBeMail/assets/134808112/b2d1ede0-d9e3-4de3-b1e7-77e92eeb3407">



### Step6: Enter an *App name* and Click on *Create*.

<img width="488" alt="image" src="https://github.com/NFA26/CanBeMail/assets/134808112/0bbf1c61-f41f-43c0-80fd-923ec9b8389a">



### Step7: Copy and Save the *Generated App Password*. To log in to CanBeMail, enter that password into the "password" field.

<img width="448" alt="image" src="https://github.com/NFA26/CanBeMail/assets/134808112/cb1ded02-1d23-451b-a9f0-8215dda25764">


## How To Install
You need to install the following Python libraries before running the application.

* PySimpleGUI
* mysql.connector
* Crypto
* cryptography

(other libraries already included in pip)

You can install the required libraries by running the following comment in a terminal or an IDE.

* To install all the required packages at once: 
pip install -r requirements.txt

## Before Start
You need to add database details to the code for your usage.

At CanBeMail/Controller/MainPageController.py Line 25
You need to write your own database information.

Finally, by running the following command, you can run the app, or if you use an IDE, you can directly click on the "run" button on the "Launcher.py" page.
python launcher.py 


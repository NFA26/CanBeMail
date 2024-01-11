import smtplib
import sys
import os
import PySimpleGUI as sg
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import mysql.connector

os.path.normpath(os.getcwd() + os.sep + os.pardir)
sys.path.insert(1,os.getcwd())
from GUI import SendMail as smg
from Controller import MainPageCl as mpc

class sendMailController():
    def __init__(self,mail_address,passw,host,mydb,mycursor):
        self.mail_address=mail_address
        self.passw=passw
        self.host=host
        self.mydb=mydb
        self.mycursor=mycursor
        
    def generate_keys(self,num):
        modulus_length = num
        key = RSA.generate(modulus_length)
        pub_key = key.publickey()
        private_key = key.exportKey()
        public_key = pub_key.exportKey()
        return private_key, public_key

    def encyrpAgRSA(self, message, public_key):
        
        
        public_key=RSA.import_key(public_key)
               
        session_key = get_random_bytes(16)

        
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(message)
        
        body = enc_session_key + cipher_aes.nonce + tag + ciphertext
        
        return body
    
    def getPublicKey(self, toAddr):
        
        self.mycursor.execute("SELECT pbKey FROM pb WHERE MailAddr=%s",(toAddr,))
        res=self.mycursor.fetchall()

        if len(res)==0:
            priv, sub=self.generate_keys(1024)
            pbkey=sub
            
            prKey=priv
            self.mycursor.execute("INSERT INTO pb (mailAddr, pbKey) VALUES (%s,%s)",(toAddr, pbkey))
            self.mycursor.execute("INSERT INTO pr (mailAddr, prKey) VALUES (%s,%s)",(toAddr, prKey))
            self.mydb.commit()
            self.mycursor.execute("SELECT pbKey FROM pb WHERE MailAddr=%s",(toAddr,))
            res=self.mycursor.fetchall()
            

        a=res[0]
        b=str(a)[13:] 
        keyyy=b[:-4]
        keyyy=keyyy.replace("\\n","""
        """)
        return keyyy
        

    def sendMailTo(self,toAddr,subject,message):
        a=toAddr.split(', ')
        public_keys=[]
        for addr in a:
            public_keys.append(self.getPublicKey(toAddr))
        
        
        
        tonew=', '.join(a)

        key = Fernet.generate_key()
        f = Fernet(key)
        input_string = message
        encrypted_string = f.encrypt(input_string.encode())
        sendstr = key+encrypted_string
        
        
        encmes=self.encyrpAgRSA(sendstr, public_keys[0])
        
        c=int.from_bytes(encmes,byteorder='little')
        c=str(c)+"//"+str(len(encmes))
        
        msg=MIMEText(c)
        
        msg['Subject']="CanBeMail: "+subject
        msg['From']=self.mail_address
        msg['To']=tonew
        
        for i in range(len(public_keys)):
            
            self.host.sendmail(self.mail_address,a[i],msg.as_string())
        

    def openPage(self):
        view=smg.createWindow()
        while True:
            events,values=view.read()
            if (events =='Go Back'):
                view.close()
                break
            elif (events == 'Send Mail' ):
                if(values['To'].strip() == ''):
                    sg.popup('Missing Address','Please fill the sender space.')
                if(values['Subject']==''):
                    sg.popup('Missing Subject','Please include subject to your mail.')
                else:
                    try:
                        self.sendMailTo(values['To'],values['Subject'],values['Maildata'])
                        sg.popup('Mail Sent','Mail sent successfully')
                        view.close()
                        break
                    except Exception as err:
                        a=str(err)
                        sg.popup('Something went wrong!', a)
            elif (events== sg.WIN_CLOSED):
                view.close()
                break

        
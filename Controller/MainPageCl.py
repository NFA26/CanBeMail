import smtplib
import imaplib
import email
from email.header import decode_header
import sys
import os
import PySimpleGUI as sg
import mysql.connector

os.path.normpath(os.getcwd() + os.sep + os.pardir)
sys.path.insert(1,os.getcwd())
from GUI import MainPage as mpg
from Controller import MainPageCl as mpc
from Controller import SendMailCl as smc
from Controller import InboxCl as ic

class MainPageController():
    def __init__(self,mail_address,passw,host,imap) -> None:
        self.mail_address=mail_address
        self.passw=passw
        self.host=host
        self.imap=imap
        self.mails=[]
        self.mailssec=[]
        self.mydb=mysql.connector.connect(
            host="",
            user="",
            passwd="",
            database=""
            )
        self.mycursor=self.mydb.cursor()
    


    def openPage(self):
        view=mpg.createWindow()
        while True:
            events,values=view.read()
            if(events == 'Logout'):
                view.close()
                self.host.close()
                break
            elif(events == 'Send New Mail' ):
                send= smc.sendMailController(self.mail_address,self.passw,self.host,self.mydb,self.mycursor)
                send.openPage()
            elif(events == 'Inbox'):
                read=ic.InboxController(self.mail_address,self.passw,self.host,self.imap,self.mydb,self.mycursor)
                read.openPage()
                self.mails=[]
            elif(events == sg.WIN_CLOSED):
                view.close()
                self.host.close()
                break
        
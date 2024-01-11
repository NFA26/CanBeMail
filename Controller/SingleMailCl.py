import smtplib
import sys
import os
import PySimpleGUI as sg
import imaplib
import email

os.path.normpath(os.getcwd() + os.sep + os.pardir)
sys.path.insert(1,os.getcwd())
from GUI import SingleMail as smg


class SingleMailController():
    def __init__(self,text) -> None:
        self.text=text

    def openPage(self):
        view=smg.createWindow(self.text)
        while True:
            events, values=view.read()
            view.refresh()
            if(events==sg.WIN_CLOSED):
                view.close()
                break


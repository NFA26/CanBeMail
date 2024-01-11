import smtplib
import sys
import os
import PySimpleGUI as sg
import imaplib
import email

os.path.normpath(os.getcwd() + os.sep + os.pardir)
sys.path.insert(1,os.getcwd())
from GUI import LoginPage as loginPage
from Controller import MainPageCl as mpc



class LoginPageController():
    def __init__(self) -> None:
        super().__init__()
        self.host=smtplib.SMTP("smtp.gmail.com",587)
        self.host.ehlo()
        self.host.starttls()
        self.imap=imaplib.IMAP4_SSL("imap.gmail.com")
    
    def loginCheck(self, mail, passw):
        try:
            self.host.login(mail,passw)
            self.imap.login(mail,passw)
            return True  
        except smtplib.SMTPAuthenticationError:
            pass
        except smtplib.SMTPException:
            pass

    


    def openPage(self):
        view=loginPage.createWindow()
        while True:
            events, values = view.read()   

            if(events == 'LOGIN'):
                mail_address = values['Mail']
                user_password = values['Password']
                if(self.loginCheck(mail_address,user_password)):
                    view.close()
                    main = mpc.MainPageController(mail_address,user_password,self.host,self.imap)
                    main.openPage()
                    break
                elif(mail_address == "" or user_password==""):
                    sg.popup('Missing Info','Please fill your information first.')
                else:
                    sg.popup('Wrong Info','Wrong Id or Password! try again.')
                continue
            elif(events == sg.WIN_CLOSED):
                view.close()
                break
                
        view.close()


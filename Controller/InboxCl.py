import smtplib
import imaplib
import email
from email.header import decode_header
import webbrowser
import mysql.connector
import sys
import os
import PySimpleGUI as sg
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from cryptography.fernet import InvalidToken
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes


os.path.normpath(os.getcwd() + os.sep + os.pardir)
sys.path.insert(1,os.getcwd())
from GUI import Inbox as inb
from Controller import SingleMailCl as smc
from Controller import MainPageCl as mpc

class InboxController():
    def generate_keys(self,num):
        modulus_length = num
        key = RSA.generate(modulus_length)
        pub_key = key.publickey()
        private_key = key.exportKey()
        public_key = pub_key.exportKey()
        return private_key, public_key
    
    def __init__(self,mail_address,passw,host,imap,mydb,cursor):
        self.mail_address=mail_address
        self.passw=passw
        self.host=host
        self.imap=imap
        self.mailssub=[]
        self.maildic={}
        self.mydb=mydb
        self.cursor=cursor
        self.cursor.execute("SELECT prKey FROM pr WHERE MailAddr=%s",(mail_address,))
        self.res=self.cursor.fetchall()
        if len(self.res)==0:
            priv, sub=self.generate_keys(1024)
            pbkey=sub
            
            prKey=priv
            self.cursor.execute("INSERT INTO pb (mailAddr, pbKey) VALUES (%s,%s)",(mail_address, pbkey))
            self.cursor.execute("INSERT INTO pr (mailAddr, prKey) VALUES (%s,%s)",(mail_address, prKey))
            self.mydb.commit()
            self.cursor.execute("SELECT pbKey FROM pb WHERE MailAddr=%s",(mail_address,))
            self.res=self.cursor.fetchall()
        
        a=self.res[0]
        b=str(a)[13:] 
        keyyy=b[:-4]
        keyyy=keyyy.replace("\\n","""
        """)
        self.prKey=keyyy

    def prEncode(self, body):
        print("1")
        private_key=RSA.import_key(self.prKey)
        print("2")
        enc_session_key = body[:private_key.size_in_bytes()]
        print(enc_session_key)
        nonce = body[private_key.size_in_bytes():private_key.size_in_bytes()+16]
        print("4")
        tag = body[private_key.size_in_bytes()+16:private_key.size_in_bytes()+16+16]
        print("5")
        ciphertext = body[private_key.size_in_bytes()+16+16:]
        print("6")	
        #### RSA decrypt
        cipher_rsa = PKCS1_OAEP.new(private_key)
        print("7")
        session_key = cipher_rsa.decrypt(enc_session_key)
        print("8")
        #### AES decrypt	
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        print("9")
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        print("10")
        return data.decode("utf-8")    

    def encdecoder(self, text):
        print("Decrypting text:", text)

        try:
            # Extract key (modify based on your key retrieval method)
            key = text[:44]

            # Decode before decryption
            decrypted_bytes = Fernet(key).decrypt(text[44:].encode())

            # Decode after decryption
            decrypted_string = decrypted_bytes.decode()

            print("Decrypted string:", decrypted_string)
            return decrypted_string

        except InvalidToken as e:
            print("Decryption Error (InvalidToken):", e)
            return None
        except Exception as e:
            print("Decryption Error (General):", e)
            return None
    def InboxRead(self,maillist,n):
        status,messages =self.imap.select("INBOX")
        N = n
        messages=int(messages[0])
        for i in range(messages,messages-N, -1):
            res, msg = self.imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg=email.message_from_bytes(response[1])
                    
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)
                    
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    
                    

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain":
                                mailunit= From+" "+subject
                                self.mailssub.append(mailunit)
                                if "CanBeMail:" in subject:
                                    try:
                                        print("bura")
                                        body=self.prEncode(body)
                                        print("if CanBeMail in subject")
                                        nbody=self.encdecoder(body)
                                        print("if CanBeMail in subject 2")
                                        self.maildic[mailunit]= nbody
                                        print("if CanBeMail in subject 3")
                                    except Exception as e:
                                        print(e)
                                        pass
                                else:
                                    self.maildic[mailunit]= body
                    else:
                        content_type = msg.get_content_type()
                        try:
                            body = msg.get_payload(decode=True).decode()
                        except Exception:
                            continue
                        if content_type == "text/plain":
                            mailunit= From+" "+subject
                            self.mailssub.append(mailunit)
                            if "CanBeMail:" in subject:
                                try:
                                    
                                    
                                    a=body.split("//")
                                    k=int(a[0]).to_bytes(int(a[1]),'little')
                                    body=self.prEncode(k)
                                    print("if CanBeMail in subject 4")
                                    nbody=self.encdecoder(body)
                                    print("if CanBeMail in subject 5")
                                    self.maildic[mailunit]= nbody
                                    print("if CanBeMail in subject 6")
                                except Exception as e:
                                    print(e)
                                    pass
                            else:
                                self.maildic[mailunit]= body
                                

                    

    def openPage(self):
        view=inb.createWindow()
        while True:
            events,values=view.read()
            if (events==sg.WIN_CLOSED):
                view.close()
                break
            elif(events=='Get Mails'):
                self.mailssub=[]
                self.maildic={}
                self.InboxRead(1,25)
                print("inbox called")
                inb.get_mails(view,self.mailssub)    
            elif(events=='Exit'):
                view.close()
                break
            elif(events=='Read Selected Mail'):
                try:
                    txtToRead=self.maildic[values['ListBox'][0]]
                    print("read selected mail called")
                    mailview=smc.SingleMailController(txtToRead)
                    print("singlemailcontroller txtToRead")
                    mailview.openPage()
                    print("a")
                except:
                    mailview=smc.SingleMailController("Can't readable from this app.")
                    mailview.openPage()
                

            



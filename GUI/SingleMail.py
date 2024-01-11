import PySimpleGUI as sg 

def createWindow(te):
        sg.theme('LightGreen6')

        layout = [    
                [sg.Multiline(default_text=te,disabled=True,key='MailBody',justification='center',size=(60,16),font=("Arial",12))]
                ]
                       
        window_icon = 'handcuff.ico' 
        window = sg.Window('CanBeMail', layout,input, size=(600,500),element_justification='c',icon = window_icon)
        return window



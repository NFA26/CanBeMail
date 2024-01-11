import PySimpleGUI as sg 

def createWindow():
        sg.theme('LightGreen6')   # select theme     


        layout = [
                [],      
                [sg.Text('To', size=(12,1),justification='center'),sg.InputText(key='To')],
                [sg.Text('Subject',size=(12,1),justification='center'),sg.InputText(key='Subject')],
                [sg.Multiline(key='Maildata',justification='center',size=(60,16))],
                [sg.Button('Send Mail', size = (10, 2),font=("Lucida",12,'bold'),pad=(200,10))],
                [sg.Button('Go Back', size = (10, 1),font=("Arial",12,'bold'), pad=(10,10), button_color='Dark Grey')]
                ]

        window_icon = 'handcuff.ico' 
        window = sg.Window('CanBeMail', layout, size=(600,500),icon=window_icon)  
        return window

#a=createWindow()
#a.read()
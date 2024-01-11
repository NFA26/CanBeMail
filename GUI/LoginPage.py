import PySimpleGUI as sg

def createWindow():

    sg.theme('LightGreen6')

    layout=[
        [sg.Image(filename="handcuff.png")],
        [sg.Text('WELCOME TO CanBeMail',size=(200,1),justification='center')],
        [sg.Text('Mail Address', size=(12,1),justification='center'),sg.InputText(key='Mail')],
        [sg.Text('Password',size=(12,1),justification='center'),sg.InputText(key='Password',password_char='*')],
        [sg.Button('LOGIN', size = (10, 1),font=("Lucida",12,'bold'))]
    ]
    
    window_icon = 'handcuff.ico' 

    window=sg.Window('CanBeMail', layout, size=(300,270), element_justification='c',icon= window_icon)

    return window

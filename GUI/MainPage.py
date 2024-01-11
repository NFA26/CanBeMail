import PySimpleGUI as sg 

def createWindow():
        sg.theme('LightGreen6')

        layout = [ 
                [sg.Button('Send New Mail', size = (25, 1),font=("Arial",12,'bold'), pad=(25,25))],
                [sg.Button('Inbox', size = (25, 1),font=("Arial",12,'bold'), pad=(25,25))],
                [sg.Button('Logout', size = (10, 1),font=("Arial",12,'bold'), pad=(25,25), button_color='Dark Grey')]

                ]
                       
        window_icon = 'handcuff.ico' 
        window = sg.Window('CanBeMail', layout,input, size=(500,600),element_justification='c',icon=window_icon)
        return window
import PySimpleGUI as sg 

def createWindow():
        sg.theme('LightGreen6')

        layout = [
                [sg.Button('Get Mails', size = (20, 1),font=("Arial",12,'bold'), pad=(25,25)),sg.Button('Read Selected Mail', size = (20, 1),font=("Arial",12,'bold'), pad=(25,25))],    
                [sg.Listbox([],s=(60,15) ,enable_events=True, horizontal_scroll=True,font=("Arial",12),key=('ListBox'))],
                [sg.Button('Exit', size = (10, 1),font=("Arial",12,'bold'), pad=(25,25), button_color='Dark Grey')]
                ]
                       
        window_icon = 'handcuff.ico' 
        window = sg.Window('CanBeMail', layout,input, size=(600,500),element_justification='c',icon= window_icon)
        return window

def get_mails(window, mails):
    window['ListBox'].update(values=mails)

a=createWindow()

                
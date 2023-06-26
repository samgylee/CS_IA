import PySimpleGUI as sg
import hashlib

def protect():
    layout = [
        [sg.Text("Enter your username:"), sg.Input(key="-EMAIL-", do_not_clear=False, size=(30,1)),],
        [sg.Text("Enter Password", size =(15,1)), sg.InputText('', key='-PASSWORD-', password_char='*',size=(15,1))]
        [sg.Button("Submit"), sg.Button("Exit")]

         ]

password_window = sg.Window('Login', layout, modal=True)





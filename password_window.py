import PySimpleGUI as sg
import hashlib


layout = [
        [sg.Text("Enter your Email address:"), sg.Input(key="-EMAIL-", do_not_clear=False, size=(30, 1))],
        [sg.Text("Enter Password", size=(15, 1)), sg.InputText('', key='-PASSWORD-', password_char='*', size=(15, 1))],
        [sg.Button("Submit"), sg.Button("Exit")]

    ]

password_window = sg.Window('Login', layout, modal=True)

#don't use him for IB

def verify_password(password):
    pass


def verify_email_address(email_input_value):
    pass


while True:
    event,values = password_window.read()
    if event == "Exit" or event == sg.WINDOW_CLOSED:
        exit()
    elif event == "submit":
        email_input_value = values['-EMAIL-']
        password_input_value = values['-PASSWORD']
        if verify_password(password_input_value) and verify_email_address(email_input_value):
            break
        else:
            continue

    password_window.close()






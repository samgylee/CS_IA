import PySimpleGUI as sg
import hashlib


def protect():
    layout = [
        [sg.Text("Enter your Email address:"), sg.Input(key="-EMAIL-", do_not_clear=False, size=(30, 1))],
        [sg.Text("Enter Password", size=(15, 1)), sg.InputText('', key='-PASSWORD-', password_char='*', size=(15, 1))],
        [sg.Button("Submit"), sg.Button("Exit")]]


    password_window = sg.Window('Login', layout, modal=True)

#don't use him for IB

    def verify_password(password):
        hash = '85b37832ed953d79b1cb6b8b03fd3fc6f8aff7f6b3edb49a759886e76321b4df'
        password_utf = password.encode('utf-8')
        password_hash= hashlib.sha256(password_utf).hexdigest()
        if hash == password_hash:
            return True
        return False


    def verify_email_address(email_address):
        user_email_address = ['jyonlee@gmail.com', 'samgylee@gmail.com']
        if email_address in user_email_address:
            return True
        return False


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






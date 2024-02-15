
import PySimpleGUI as sg
import hashlib


# Define a function named 'protect' to create a password protection window.
# This function can be imported and used in other scripts, such as 'database.py'.
def protect():
    # Define the layout of the password protection window
    layout = [
        [sg.Text("Enter your Email address:"), sg.Input(key="-EMAIL-", do_not_clear=False, size=(30, 1))],
        [sg.Text("Enter Password:", pad=(27, 0)), sg.InputText('', key='-PASSWORD-', password_char='*', size=(30, 1))],
        [sg.Button("Submit"), sg.Button("Exit")]
    ]

    # Create the password protection window using PySimpleGUI
    password_window = sg.Window('Login', layout, modal=True)

# function to verify password by converting into hash, the password is jung my mother's name
    def verify_password(password):
        # Stored hash for the correct password ('jung' hashed with SHA-256)
        stored_hash = '85b37832ed953d79b1cb6b8b03fd3fc6f8aff7f6b3edb49a759886e76321b4df'

        # Encode the password as UTF-8 and hash it using SHA-256
        password_utf = password.encode('utf-8')
        password_hash = hashlib.sha256(password_utf).hexdigest()

        # Compare the calculated hash with the stored hash
        if password_hash == stored_hash:
            return True
        return False

# function that checks if the inputted email address is in the list.
    def verify_email_address(email_address):
        user_email_address = ['jyonlee@gmail.com', 'samgylee@gmail.com']
        if email_address in user_email_address:
            return True
        return False

    # Loop for handling the password verification process
    while True:
        # Read the password window event and values
        event, values = password_window.read()

        # Exit the application if the window is closed or "Exit" button is clicked
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            exit()

        # Proceed if the "Submit" button is clicked
        elif event == "Submit":
            # Retrieve email and password input values
            email_input_value = values['-EMAIL-']
            password_input_value = values['-PASSWORD-']

            # Check if both password and email are valid
            if verify_password(password_input_value) and verify_email_address(email_input_value):
                break  # Exit the password verification loop
            else:
                continue  # Retry password input if credentials are invalid

    password_window.close()

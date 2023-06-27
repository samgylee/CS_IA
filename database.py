import PySimpleGUI as sg
import copy
import password_window
# Function to save data to a file


def save_data_to_file(data):
    with open("data.txt", "w") as file:
        for row in data:
            file.write(",".join(row) + "\n")



sg.theme('LightBlue2')
# Function to load data from a file
def load_data_from_file():
    try:
        with open("data.txt", "r") as file:
            data = file.readlines()
            data = [row.strip().split(",") for row in data]
            return data
    except FileNotFoundError:
        return []

# Function to convert total grade to letter grade


def convert_to_letter_grade(total_grade):
    if total_grade >= 90:
        return "A"
    elif total_grade >= 80:
        return "B"
    elif total_grade >= 70:
        return "C"
    elif total_grade >= 60:
        return "D"
    elif total_grade >= 50:
        return "E"
    else:
        return "F"


# Function to rank students based on total grades
def rank_students():
    rank_students_list = copy.deepcopy(students_data)
    rank_students_list.sort(key=lambda x: int(x[4]), reverse=True,)
    return rank_students_list


students_data = load_data_from_file()


ranking_1 = rank_students()

tab_3_list = []

for index, row in enumerate(ranking_1):
    tab_3_list.append([str(index+1), row[0], row[4], row[5]])



# Layout for Tab 1
tab1_layout = [
    [sg.Text('Student name'),sg.InputText(key="count-name", size=(18,0))],
    [sg.Text('Homework grade'),sg.InputText(key="homework-grade",size=(15,0))],
    [sg.Text('Midterm grade'),sg.InputText(key="midterm-grade",size=(17,0))],
    [sg.Text('Final grade'),sg.InputText(key="final-grade",size=(19,0), )],
    [sg.Button("Add Student")]
]

# Layout for Tab 2
tab2_layout = [
    [
        sg.Table(
            values=students_data,
            headings=["Name", "Homework Grade", "Midterm Grade", "Final Grade", "Total Grade"],
            key="students-table",
            col_widths=[20, 15, 15, 15, 15, 15],
            justification="center",
            num_rows=10,
            enable_events=True,
            bind_return_key=True,
            auto_size_columns=False,
            display_row_numbers=False,
            font=("Helvetica", 16)
        )
    ],
    [sg.Button("-", key="delete-button"), sg.Button("edit", key="edit-students")]

]

# Layout for Tab 3
tab3_layout = [
    [
        sg.Table(
            values=tab_3_list,
            headings=["Rank", "Name", "Total Grade", "Letter Grade"],
            key="ranked-students-table",
            justification="center",
            col_widths=[10, 20, 15, 15],
            num_rows=10,
            enable_events=True,
            bind_return_key=True,
            auto_size_columns=False,
            display_row_numbers=False,  # we want to rank the students not in row #
            font=("Helvetica", 16)  # Adjust the font size as per your preference
        )
    ]
]
tab4_layout = [

]

# Create the main window with tabs


data_layout = [
    [sg.TabGroup([
        [sg.Tab('Add Students', tab1_layout), sg.Tab('View Students', tab2_layout), sg.Tab('Student Ranking', tab3_layout), sg.Tab('Graph', tab4_layout)]
    ])],
]

data_window = sg.Window("Student DB", data_layout, modal=True)

# Load data from file
students_data = load_data_from_file()

# Event loop
while True:
    event, values = data_window.read()

    if event == sg.WINDOW_CLOSED:
        # Save data to file when closing the window
        save_data_to_file(students_data)
        break

    if event == "Add Student":
        name = values["count-name"]
        homework_grade = values["homework-grade"]
        midterm_grade = values["midterm-grade"]
        final_grade = values["final-grade"]

        try:
            total_grade = int(homework_grade) + int(midterm_grade) + int(final_grade)
            if 0 <= total_grade <= 100:
                letter_grade = convert_to_letter_grade(total_grade)
                students_data.append([name, homework_grade, midterm_grade, final_grade, str(total_grade), letter_grade])
                data_window["students-table"].update(values=students_data)
                data_window["count-name"].update("")  # Clear the name input field
                data_window["homework-grade"].update("")  # Clear the homework grade input field
                data_window["midterm-grade"].update("")  # Clear the midterm grade input field
                data_window["final-grade"].update("")  # Clear the final grade input field
                print(students_data)

            else:
                sg.popup_ok(
                    "Total grade needs to be between 0 to 100",
                    title="Error",
                    button_color="red",
                )

        except ValueError:
            sg.popup_ok(
                "Please type in Integer only.",
                title="Error",
                button_color="red",
            )

            pass

    if event == "students-table":
        selected_row = values["students-table"]
        if selected_row:
            selected_row_index = selected_row[0]
            if selected_row_index < len(students_data):
                name = students_data[selected_row_index][0]
                homework_grade = students_data[selected_row_index][1]
                midterm_grade = students_data[selected_row_index][2]
                final_grade = students_data[selected_row_index][3]
                data_window["count-name"].update(name)  # Update the name input field
                data_window["homework-grade"].update(homework_grade)  # Update the homework grade input field
                data_window["midterm-grade"].update(midterm_grade)  # Update the midterm grade input field
                data_window["final-grade"].update(final_grade)  # Update the final grade input field

    if event == "delete-button":
        selected_row = values["students-table"]
        if selected_row:
            selected_row_index = selected_row[0]
            if selected_row_index < len(students_data):
                removed_row = students_data.pop(selected_row_index)
                data_window["students-table"].update(values=students_data)

    if event == "edit-students":
        selected_row = values["students-table"]
        print(selected_row)


    ranking_2 = rank_students()

    data_window["ranked-students-table"].update(values=[[str(index+1),row[0], row[4], row[5]] for index, row in enumerate(ranking_2)]
        )

data_window.close()

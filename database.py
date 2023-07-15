import PySimpleGUI as sg
import copy
import password_window
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_figure(canvas, figure): #tkinter canvas widget, bargraph object plt
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas) # type = Class FigureCanvasTkAgg
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


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
    rank_students_list.sort(key=lambda x: int(x[4]), reverse=True)
    return rank_students_list


def grading_students(name, homework_grade, midterm_grade, final_grade, exclude_name=None):
    try:
        total_grade = int(homework_grade) + int(midterm_grade) + int(final_grade)
        if 0 <= total_grade <= 100:
            if exclude_name:
                if any(row[0] == name and row[0] != exclude_name for row in students_data):
                    return None
            else:
                if any(row[0] == name for row in students_data):
                    return None

            letter_grade = convert_to_letter_grade(total_grade)
            return total_grade
        else:
            return None
    except ValueError:
        return None


students_data = load_data_from_file()


ranking_1 = rank_students()

tab_3_list = []

for index, row in enumerate(ranking_1):
    tab_3_list.append([str(index + 1), row[0], row[4], row[5]])

student_total_grades = []  # new list
# total grades from rank_students_list
for row in ranking_1:
    total_grade = row[4]
    student_total_grades.append(total_grade)

# Sort descending order
student_total_grades.sort(reverse=True)

# Print the sorted total grades
print(student_total_grades)
# Initialize the grade count dictionary
grade_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}

# Iterate over the total grades and update the grade count
for total_grade in student_total_grades:
    total_grade = int(total_grade)  # Convert the total grade to an integer
    if total_grade >= 90:
        grade_count['A'] += 1
    elif total_grade >= 80:
        grade_count['B'] += 1
    elif total_grade >= 70:
        grade_count['C'] += 1
    elif total_grade >= 60:
        grade_count['D'] += 1
    elif total_grade >= 50:
        grade_count['E'] += 1
    else:
        grade_count['F'] += 1

# Print the grade count# Create the student numbers list in alphabetical order
student_numbers = [grade_count[grade] for grade in sorted(grade_count.keys())]
#
# # Print the student numbers list
print(student_numbers)


grade = ['A', 'B', 'C', 'D', 'E', 'F']


# create a loop that will add the corresponding student numbers per grade, then create 'student numbers' array with correct positioning

def create_bar_graph(grade, student_numbers):
    plt.figure(figsize=(4,2.5))
    plt.bar(grade, student_numbers, color='red', width=0.4)
    plt.title('Grade vs Student number', fontsize=10)
    plt.xlabel('Grade', fontsize=10)
    plt.ylabel('student number', fontsize=10)
    return plt.gcf()


# Layout for Tab 1
tab1_layout = [
    [sg.Text('Student name'), sg.InputText(key="count-name", size=(15, 0), pad=(20, 0))],
    [sg.Text('Homework grade'), sg.InputText(key="homework-grade", size=(15, 0))],
    [sg.Text('Midterm grade'), sg.InputText(key="midterm-grade", size=(15, 0), pad=(17, 0))],
    [sg.Text('Final grade'), sg.InputText(key="final-grade", size=(15, 0), pad=(32, 0))],
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
            font=("Helvetica", 16),
            expand_x=True
        )
    ],
    [sg.Button("-", key="delete-button"), sg.Button("edit", key="edit-students"), sg.Button("Sort", key="sort-button")]

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
            font=("Helvetica", 16),
            expand_x=True

        )
    ]
]
tab4_layout = [
    [sg.Column([[sg.Canvas(key='bar-graph', size=(400, 400))]], element_justification='center', pad=(150, 100))]
]


# Create the main window with tabs

data_layout = [
    [sg.TabGroup([
        [sg.Tab('Add Students', tab1_layout), sg.Tab('View Students', tab2_layout),
         sg.Tab('Student Ranking', tab3_layout), sg.Tab('Graph', tab4_layout)]
    ], enable_events=True, expand_x=True, expand_y=True)]]

data_window = sg.Window("Student DB", data_layout, modal=True, resizable=True, finalize=True)
# Load data from file
students_data = load_data_from_file()

bar_graph=draw_figure(data_window["bar-graph"].TKCanvas, create_bar_graph(grade, student_numbers))


def update_bar_graph(bar_graph):
    bar_graph.get_tk_widget().forget() #forgets bar_graph
    bar_graph = draw_figure(data_window["bar-graph"].TKCanvas, create_bar_graph(grade, student_numbers))
    return bar_graph

    #forgets the old graph and draws a new graph with the new data

# password_window.protect()
# Event loop
while True:

    event, values = data_window.read()
    print(event)
    if event == sg.WINDOW_CLOSED:
        # Save data to file when closing the window
        save_data_to_file(students_data)
        break

    if event == "Add Student":
        name = values["count-name"]
        homework_grade = values["homework-grade"]
        midterm_grade = values["midterm-grade"]
        final_grade = values["final-grade"]

        total_grade = grading_students(name, homework_grade, midterm_grade, final_grade)
        if total_grade is None:
            sg.popup_error(
                "Please check if your input is correct",
                title="Error",
                button_color="red",
            )
        else:
            letter_grade = convert_to_letter_grade(total_grade)
            students_data.append(
                [name, homework_grade, midterm_grade, final_grade, str(total_grade), letter_grade])
            data_window["students-table"].update(values=students_data)
            data_window["count-name"].update("")  # Clear the name input field
            data_window["homework-grade"].update("")  # Clear the homework grade input field
            data_window["midterm-grade"].update("")  # Clear the midterm grade input field
            data_window["final-grade"].update("")  # Clear the final grade input field



    if event == "students-table":
        selected_row = values["students-table"]
        if selected_row:
            selected_row_index = selected_row[0]
            if selected_row_index < len(students_data):
                name = students_data[selected_row_index][0]
                homework_grade = students_data[selected_row_index][1]
                midterm_grade = students_data[selected_row_index][2]
                final_grade = students_data[selected_row_index][3]
    if event == "delete-button":
        selected_row = values["students-table"]
        if selected_row:
            selected_row_index = selected_row[0]
            if selected_row_index < len(students_data):
                removed_row = students_data.pop(selected_row_index)
                data_window["students-table"].update(values=students_data)


    if event == "sort-button":
        students_data = sorted(students_data, key=lambda x: x[0].lower())
        data_window["students-table"].update(values=students_data)

    if event == "edit-students":
        selected_row = values["students-table"]
        if selected_row:
            selected_row_index = selected_row[0]
            if selected_row_index < len(students_data):
                name = students_data[selected_row_index][0]
                homework_grade = students_data[selected_row_index][1]
                midterm_grade = students_data[selected_row_index][2]
                final_grade = students_data[selected_row_index][3]
                edit_layout = [
                    [sg.Text('Name:'), sg.Input(key='edit-name', default_text=name)],
                    [sg.Text('Homework Grade:'), sg.Input(key='edit-homework', default_text=homework_grade)],
                    [sg.Text('Midterm Grade:'), sg.Input(key='edit-midterm', default_text=midterm_grade)],
                    [sg.Text('Final Grade:'), sg.Input(key='edit-final', default_text=final_grade)],
                    [sg.Button('Save')]
                ]

                edit_window = sg.Window('Edit Student', edit_layout)

                while True:
                    edit_event, edit_values = edit_window.read()

                    if edit_event == sg.WINDOW_CLOSED:
                        break

                    if edit_event == 'Save':
                        new_name = edit_values['edit-name']
                        new_homework_grade = edit_values['edit-homework']
                        new_midterm_grade = edit_values['edit-midterm']
                        new_final_grade = edit_values['edit-final']

                        # convert input grades to int
                        new_homework_grade = int(new_homework_grade)
                        new_midterm_grade = int(new_midterm_grade)
                        new_final_grade = int(new_final_grade)

                        total_grade = grading_students(new_name, new_homework_grade, new_midterm_grade,
                                                       new_final_grade,
                                                       exclude_name=name)
                        if total_grade is None:
                            sg.popup_error(
                                "Please check if your input is correct",
                                title="Error",
                                button_color="red",
                            )
                        else:
                            students_data[selected_row_index][0] = new_name
                            students_data[selected_row_index][1] = str(new_homework_grade)
                            students_data[selected_row_index][2] = str(new_midterm_grade)
                            students_data[selected_row_index][3] = str(new_final_grade)
                            students_data[selected_row_index][4] = str(total_grade)
                            students_data[selected_row_index][5] = convert_to_letter_grade(total_grade)




                        break

                edit_window.close()

    bar_graph = update_bar_graph(bar_graph)
data_window.close()

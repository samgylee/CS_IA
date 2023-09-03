import PySimpleGUI as sg
import copy
import password_window
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Any, List, Tuple
# Global Variables

# create the empty tab 3 list
tab_3_list: List[List[str]] = []
# Empty students data for creating the rank students later on
students_data: List[List[str]] = []
# empty list for the first ranking
ranking_1: List[List[str]] = []
# empty list for the second ranking after deep-copying students data whenever tab 3 is updated every loop
ranking_2: List[List[str]] = []
# empty list for the grades that will be stored to be represented in the bar-graph for visual representation.
grade: list[str] = ['A', 'B', 'C', 'D', 'E', 'F']
# empty list for the number of students in each grade.
# Set in the  index starting from A,B,C,D,etc. For example, if the list has 5,2,3, A=5,B=2,C=3 students in each grade.
student_numbers: List[int] = []
# Initialize empty histogram to visually represent the number of students in each grade in a different tab
bar_graph = None
# initialize the window
data_window = None


# Function to draw a figure on a canvas widget
def draw_figure(canvas, figure):  # tkinter canvas widget, bargraph object plt
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)  # type = Class FigureCanvasTkAgg
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# Function to save data to a file
def save_data_to_file(data: List[List[str]]):
    with open("data.txt", "w") as file:
        for row in data:
            file.write(",".join(row) + "\n")


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
def convert_to_letter_grade(total_grade: int):
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


# Function to perform bubble sort on data
def bubble_sort(data: List[List[str]]):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Compare the names for alphabetical order by making them lowercase
            if data[j][0].lower() > data[j + 1][0].lower():
                data[j], data[j + 1] = data[j + 1], data[j]


# Function to perform grading for students
def grading_students(name: str, homework_grade: int, midterm_grade: int, final_grade: int, exclude_name=None):
    try:
        total_grade = int(homework_grade) + int(midterm_grade) + int(final_grade)
        if 0 <= total_grade <= 100:
            if exclude_name:
                if any(row[0] == name and row[0] != exclude_name for row in students_data):
                    return None
            else:
                if any(row[0] == name for row in students_data):
                    return None

            return total_grade
        else:
            return None
    except ValueError:
        return None


# Function to rank students based on total grades
def rank_students():
    rank_students_list: list[Any] = copy.deepcopy(students_data)
    n = len(rank_students_list)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if int(rank_students_list[j][4]) < int(rank_students_list[j + 1][4]):
                rank_students_list[j], rank_students_list[j + 1] = rank_students_list[j + 1], rank_students_list[j]

    return rank_students_list


# Function to update student numbers based on grades for plotting the bar graph
def update_student_numbers(ranking: List[List[str]]):
    # Calculate total grades from rank_students_list
    student_total_grades = []  # new list
    grade_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}  # create a new dictionary for the grades

    # total grades from rank_students_list
    for row in ranking:
        total_grade = row[4]
        student_total_grades.append(total_grade)

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

    # create a loop that will add the corresponding student numbers per grade, then create 'student numbers' array with correct positioning
    n = len(grade)
    for i in range(n):
        for j in range(0, n - i - 1):
            if grade[j] > grade[j + 1]:
                grade[j], grade[j + 1] = grade[j + 1], grade[j]

    student_numbers = [grade_count[grade] for grade in grade]

    return student_numbers


# function for creating the bargraph that will visualize the rankings in Letter grades,
# by plotting grades A-F in the x axis and the number of students in that criteria in the y axis
def create_bar_graph(grade, student_numbers):
    plt.figure(figsize=(4, 2.5), facecolor='#AAB6D3')
    ax = plt.axes()
    ax.set_facecolor("white")
    plt.bar(grade, student_numbers, color='red', width=0.4)
    plt.title('Grade vs Student Number', fontsize=10)
    plt.xlabel('Grade', fontsize=10)
    plt.ylabel('Student Number', fontsize=10)
    plt.subplots_adjust(top=0.9, bottom=0.2)

    return plt.gcf()

# forget the old graph and draws a new graph with the new data
def update_bar_graph(bar_graph):
    bar_graph.get_tk_widget().forget()  # forgets bar_graph
    bar_graph = draw_figure(data_window["bar-graph"].TKCanvas, create_bar_graph(grade, student_numbers))
    return bar_graph

# Now we are done with declaring our global functions, now this is the main body of the code.

# import PysimpleGui Themes, and set the theme to a prettier light blue
sg.theme('LightBlue2')

# Load data from file using the load_data procedure.
students_data = load_data_from_file()

# rank the students using the imported data , so it shows the initial ranking when we open the code. This will change whenever the user makes a change in the program.
ranking_1 = rank_students()

# for loop to add to the new tab 3 list the rankings of the students
for index, row in enumerate(ranking_1):
    tab_3_list.append([str(index + 1), row[0], row[4], row[5]])

# Prepare data for bar graph
student_numbers = update_student_numbers(ranking_1)

# Layout for Tab 1 where you input  new students, added paddings so they align to each other more neatly.
tab1_layout = [
    [sg.Text('Student name'), sg.InputText(key="count-name", size=(15, 0), pad=(20, 0))],
    [sg.Text('Homework grade'), sg.InputText(key="homework-grade", size=(15, 0))],
    [sg.Text('Midterm grade'), sg.InputText(key="midterm-grade", size=(15, 0), pad=(17, 0))],
    [sg.Text('Final grade'), sg.InputText(key="final-grade", size=(15, 0), pad=(32, 0))],
    [sg.Button("Add Student")]
]

# Layout for Tab 2 that shows the students in the students_data list,
# this is where the user can edit the students, delete them and sort them in alphabetical order
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
    [sg.Button("-", key="delete-button"), sg.Button("Edit", key="edit-students"), sg.Button("Sort", key="sort-button")]

]

# Layout for Tab 3 that ranks the students
# This page automatically updates every loop until the program is closed.
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

# layout for tab 4 that draws a canvas for the visual histogram.
# This helps the viewer see a normal distribution, and the bell curve of the grades.
tab4_layout = [
    [sg.Column([[sg.Canvas(key='bar-graph', size=(400, 400))]], element_justification='center', pad=(150, 100))]
]

# Create the main window with tabs
data_layout = [
    [sg.TabGroup([
        [sg.Tab('Add Students', tab1_layout), sg.Tab('View Students', tab2_layout),
         sg.Tab('Student Ranking', tab3_layout), sg.Tab('Graph', tab4_layout)]
    ], enable_events=True, expand_x=True, expand_y=True)]]

# imports the password window to prevent access to the code from an unauthorized person
password_window.protect()

# sets the window layout. Finalize=True is needed for the matplotlib graph.
data_window = sg.Window("Student DB", data_layout, modal=True, resizable=True, finalize=True)
# Load data from file
students_data = load_data_from_file()

# draws the first bargraph so it doesn't override the password window
bar_graph = draw_figure(data_window["bar-graph"].TKCanvas, create_bar_graph(grade, student_numbers))


# Event loop
while True:

    event, values = data_window.read()

    if event == sg.WINDOW_CLOSED:
        # Save data to file when closing the window
        save_data_to_file(students_data)
        break
    # When the user clicks add student, it assigns the variables to the values and gives them keys to be checked later if the vlaues are correct.
    if event == "Add Student":
        name = values["count-name"]
        homework_grade = values["homework-grade"]
        midterm_grade = values["midterm-grade"]
        final_grade = values["final-grade"]
        # uses the grading students function to see if the values are valid and if not, pops up a error message.
        # If the values are valid, appends the new student to the students data list and refreshes the window.
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
    # enables the user to select the tables
    if event == "students-table":
        selected_row = values["students-table"]
        if selected_row:
            selected_row_index = selected_row[0]
            if selected_row_index < len(students_data):
                name = students_data[selected_row_index][0]
                homework_grade = students_data[selected_row_index][1]
                midterm_grade = students_data[selected_row_index][2]
                final_grade = students_data[selected_row_index][3]
    # when the user clicks the sort button, sorts the names in alphabetical order
    if event == "sort-button":
        bubble_sort(students_data)
        data_window["students-table"].update(values=students_data)
    # when the user clicks the delete button, the program deletes the selected student's data from the file
    if event == "delete-button":
        selected_row = values["students-table"]
        if selected_row:
            selected_row_index = selected_row[0]
            if selected_row_index < len(students_data):
                removed_row = students_data.pop(selected_row_index)
                data_window["students-table"].update(values=students_data)
    # when the user clicks on the edit button, creates a new edit window that saves the changes and updates it to student_data and represents it on tab 2 and 3
    if event == "edit-students":
        selected_edit_row = values["students-table"]
        if selected_edit_row:
            selected_row_index = selected_edit_row[0]
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
                # new edit window
                while True:
                    edit_event, edit_values = edit_window.read()

                    if edit_event == sg.WINDOW_CLOSED:
                        break
                    # This is the button that allows the new changes to be saved
                    if edit_event == 'Save':
                        new_name = edit_values['edit-name']
                        new_homework_grade = edit_values['edit-homework']
                        new_midterm_grade = edit_values['edit-midterm']
                        new_final_grade = edit_values['edit-final']

                        # convert input grades to int
                        new_homework_grade = int(new_homework_grade)
                        new_midterm_grade = int(new_midterm_grade)
                        new_final_grade = int(new_final_grade)

                        total_grade = grading_students(new_name, new_homework_grade, new_midterm_grade, new_final_grade,
                                                       exclude_name=name)
                        # If the input is invalid, pops up a error message
                        if total_grade is None:
                            sg.popup_error(
                                "Please check if your input is correct",
                                title="Error",
                                button_color="red",
                            )
                        # swaps the changes if the inputs are corrects
                        else:
                            students_data[selected_row_index][0] = new_name
                            students_data[selected_row_index][1] = str(new_homework_grade)
                            students_data[selected_row_index][2] = str(new_midterm_grade)
                            students_data[selected_row_index][3] = str(new_final_grade)
                            students_data[selected_row_index][4] = str(total_grade)
                            students_data[selected_row_index][5] = convert_to_letter_grade(total_grade)

                        break

                edit_window.close()
    # updates datawindow
    if event != "students-table":
        data_window['students-table'].update(values=students_data)
    # updates the ranks of the students to be correctly shown in tab 3 when the changes are made
    ranking_2 = rank_students()
    data_window["ranked-students-table"].update(
        values=[[str(index + 1), row[0], row[4], row[5]] for index, row in
                enumerate(ranking_2)])
    # updates matplotlib graph based upon the new updated ranking
    student_numbers = update_student_numbers(ranking_2)
    bar_graph = update_bar_graph(bar_graph)
data_window.close()

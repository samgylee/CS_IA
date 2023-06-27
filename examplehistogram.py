import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

grade = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
student_numbers = [10, 40, 20, 10, 6.9, 7, 0]

#try coding like the guy, instead of students array, try with letter grades.
#grades and student number on each grade

def create_bar_graph(grade, student_numbers):
    plt.figure(figsize=(10, 7))
    plt.bar(grade, student_numbers, color='red', width=0.4)
    plt.title('Grade vs Student number', fontsize=10)
    plt.xlabel('Grade', fontsize=14)
    plt.ylabel('student number', fontsize=10)
    return plt.gcf()


layout = [[sg.Text('Bar Graph')],
          [sg.Canvas(size=(900, 500), key='-CANVAS-')],
          [sg.Exit()]]


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


histogram_window = sg.Window('PySimpleGUI + MatPlotLib Bar Graphs', layout, finalize=True, element_justification='center')

draw_figure(histogram_window['-CANVAS-'].TKCanvas, create_bar_graph(grade, student_numbers))

while True:
    event, values = histogram_window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

histogram_window.close()
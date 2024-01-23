import random


#Stworzenie funkcji, ktora odpowiada za usuwanie widgetow
def clear_widgets(widgets):
    for widget_name in widgets:
        if widgets[widget_name] != []:
            widgets[widget_name][-1].hide()
        for _ in range(0, len(widgets[widget_name])):
            widgets[widget_name].pop()


#Stworzenie funkcji, ktora odpowiada za usuwanie parametrow
def clear_parameters(parameters):
    for parm in parameters:
        if parameters[parm] != []:
            for _ in range(0, len(parameters[parm])):
                parameters[parm].pop()
    parameters["random_question_index"].append(random.randint(0, 14))
    parameters["score"].append(0)
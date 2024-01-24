import random
from unittest.mock import Mock, patch


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




#_____Testy______
def test_clear_widgets():
    # Przygotowanie mocków
    widget1_mock = Mock()
    widget2_mock = Mock()

    widgets = {
        "widget1": [widget1_mock, widget1_mock, widget1_mock],
        "widget2": [widget2_mock, widget2_mock]
    }
    # Wywołanie funkcji clear_widgets z mockami
    clear_widgets(widgets)
    # Asercje
    for widget_list in widgets.values():
        for widget_mock in widget_list:
            widget_mock.hide.assert_called_once()
    # Sprawdzenie, czy listy widgetów są puste
    assert all(not widget_list for widget_list in widgets.values())


#Generowanie dekoratorem losowej wartosci do testu
@patch('random.randint', return_value=9)
def test_clear_parameters_another_case():
    parameters = {
        "param1": [4, 5],
        "param2": ["x", "y", "z"],
        "random_question_index": [8],
        "score": [20, 30, 40]
    }

    clear_parameters(parameters)

    assert all(not parameters[param] for param in parameters.keys() if param != "random_question_index" and param != "score")
    assert parameters["random_question_index"][-1] == 9  # Ustalamy, że randint zawsze zwraca 9
    assert parameters["score"][-1] == 0
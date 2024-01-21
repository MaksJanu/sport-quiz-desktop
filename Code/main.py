import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

import requests
import pandas as pd
import random
import html


#Pobieranie z API bazy pytan i odpowiedzi o sportach
def get_question_sets():
    response = requests.get(url="https://opentdb.com/api.php?amount=30&category=21&difficulty=easy&type=multiple")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data["results"])
        return df
    elif response.status_code == 404:
        return False
    
#Wywolanie funkcji aby przypisac dataframe'a do zmiennej
questions_set = get_question_sets()

#Przygotowanie odpowiedzi i pytan
def preload_data(question_index):
    question = questions_set["question"][question_index]
    correct_answer = questions_set["correct_answer"][question_index]
    wrong_answers = questions_set["incorrect_answers"][question_index]

    #Zastapienie formatowania dla znakow
    formatting = [
        ("#039", "'"),
        ("&", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">"),
    ]

    #Zastapienie zlych znakow w stringach
    for tuple in formatting:
        question = question.replace(tuple[0], tuple[1])
        correct_answer = correct_answer.replace(tuple[0], tuple[1])
    #Zastapienia zlych znakow w listach
        for tuple in formatting:
            wrong_answers = [char.replace(tuple[0], tuple[1]) for char in wrong_answers]

    parameters["question"].append(question)
    parameters["correct"].append(correct_answer)
    #Scalenie wszystkich odpowiedzi i przetasowanie
    all_answers = wrong_answers + [correct_answer]
    random.shuffle(all_answers)
    #Dodawanie odpowiedzi do parameters
    for i in range(0, 4):
        parameters[f"answer{i+1}"].append(all_answers[i])

    return all_answers

#Przechowywanie pytan i odpowiedzi w slowniku
parameters = {
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct": [],
    "score": [0],
    "random_question_index": [random.randint(0,29)],
}





#Przechowywanie instancji widgetów w listach
widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
}



#Inicjalizacja okna wraz z podstawowymi parametrami i tytułem
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Sport Quiz")
window.setFixedWidth(1000)
window.move(2700, 200)
window.setStyleSheet("background: #4d4c4d;")
#161219




#Zainicjalizowanie gridu pod widgety
grid = QGridLayout()



#Stworzenie funkcji, ktora odpowiada za usuwanie widgetow
def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for _ in range(0, len(widgets[widget])):
            widgets[widget].pop()

#Stworzenie funkcji do pokazania okna startowego(pokazanie pierwszego frame'a)
def show_frame1():
    clear_widgets()
    frame1()




#Stworzenie funkcji do startu gry(pokazanie drugiego frame'a)
def start_game():
    clear_widgets()
    preload_data(parameters["random_question_index"][-1])
    frame2()



#Stworzenie funkcji do generowania przyciskow z odpowiedziami
def answer_button(answer, l_margin, r_margin):
    #Stworzenie przyciskow dla odpowiedzi
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        "*{border: 4px solid '#292555';" +
        "border-radius: 25px;" +
        "font-size: 20px;" +
        "color: white;" +
        "padding: 15px 0;" +
        "margin-left: " + str(l_margin) + "px;" +
        "margin-right: " + str(r_margin) + "px;" +
        "margin-top: 20px;}" +
        "*:hover{background: '#292555';}"
    )
    #Przypisanie przycisku odpowiedzi do funkcji 
    button.clicked.connect(lambda x: is_correct(button))
    return button


def is_correct(btn):
    if btn.text() == parameters["correct"][-1]:
        print(f"{btn.text()} is correct")

        #Aktualizowanie score'a po poprawnej odpowiedzi
        temp_score = parameters["score"][-1]
        parameters["score"].pop()
        parameters["score"].append(temp_score + 10)

        #Losowanie kolejnego indexu dla kolejnego pytania
        parameters["random_question_index"].pop()
        parameters["random_question_index"].append(random.randint(0, 29))
        preload_data(parameters["random_question_index"][-1])

        #Aktualizowanie nazw widgetow: question i answery dla kolejnego pytania
        widgets["score"][-1].setText(str(parameters["score"][-1]))
        widgets["question"][0].setText(parameters["question"][-1])
        for i in range(1, 5):
            widgets[f"answer{i}"][0].setText(str(parameters[f"answer{i}"][-1]))
    else:
        #Wywolanie kodu po blednej odpowiedzi
        clear_widgets()
        






#Funkcja, ktora generuje strone startowa
def frame1():
    #Wrzucenie grafiki i dostosowanie stylu
    image = QPixmap("Images/sport_quiz.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;")
    #Przechowywanie loga jako instancji w liście aby miało scope globalny
    widgets["logo"].append(logo)
    #Dodanie widgetu do grida oraz umieszczenie go w kolumnie 0 i rzędzie 0
    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)

    #Dodanie widgetu przycisku i wystylizowanie go
    button = QPushButton("PLAY")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        "*{border: 4px solid '#292555';" +
        "border-radius: 30px;" +
        "font-size: 35px;" +
        "color: white;" +
        "padding: 15px 0;" +
        "margin: 100px 350px;}" +
        "*:hover{background: '#292555';}"
    )
    #Przypisanie funkcji do przycisku
    button.clicked.connect(start_game)
    #Przechowywanie przycisku jako instancji w liście aby miało scope globalny
    widgets["button"].append(button)
    #Dodanie widgetu do grida oraz umieszczenie go w kolumnie 1 i rzędzie 0
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)



#Funkcja generujaca druga strone z pytaniem, odpowiedziami i scorem
def frame2():
    #Dodanie widgetu scorea
    score = QLabel(str(parameters["score"][-1]))
    score.setAlignment(QtCore.Qt.AlignCenter)
    score.setStyleSheet(
        "font-size: 35px;" +
        "color: white;" +
        "padding: 15px 15px 15px 15px;" +
        "margin: 20px 200px;" +
        "background: '#64A314';" +
        "border: 1px solid '#64A314';" +
        "border-radius: 20px;"
    )
    widgets["score"].append(score)
    grid.addWidget(widgets["score"][-1], 0, 1)

    #Dodanie widgetu gdzie przechowywane bedzie pytanie
    question = QLabel(parameters["question"][-1])
    question.setAlignment(QtCore.Qt.AlignCenter)
    #Wrapowanie tekstu jezeli bedzie za dlugi, bedzie zapisywac go linia pod linia
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: white;" +
        "padding: 75px;"
    )
    widgets["question"].append(question)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)

    #Tworzenie przyciskow z odpowiedziami
    button1 = answer_button(parameters["answer1"][-1], 85, 5)
    button2 = answer_button(parameters["answer2"][-1], 5, 85)
    button3 = answer_button(parameters["answer3"][-1], 85, 5)
    button4 = answer_button(parameters["answer4"][-1], 5, 85)
    #Dodawanie przyciskow do list, ktore sa potrzebne do scopea globalnego
    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)
    #Dodawanie przyciskow odpowiedzi do grida
    grid.addWidget(widgets["answer1"][-1], 2, 0,)
    grid.addWidget(widgets["answer2"][-1], 2, 1,)
    grid.addWidget(widgets["answer3"][-1], 3, 0,)
    grid.addWidget(widgets["answer4"][-1], 3, 1,)

    #Wrzucenie grafiki mniejszego loga i dostosowanie stylu
    image = QPixmap("Images/sport_quiz_bottom.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "margin-top: 50px;" +
        "margin-bottom: 30px;"
    )
    #Przechowywanie loga jako instancji w liście aby miało scope globalny
    widgets["logo"].append(logo)
    grid.addWidget(widgets["logo"][-1], 4, 0, 1, 2)

frame1()









window.setLayout(grid)
#Zamknięcie okna
window.show()
sys.exit(app.exec())
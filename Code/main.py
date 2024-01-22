import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor

import requests
import pandas as pd
import random
import html

global difficulty
difficulty=""
global current_score
current_score = 0


#Pobieranie z API bazy pytan i odpowiedzi o sportach
def get_question_sets(difficulty):
    response = requests.get(url=f"https://opentdb.com/api.php?amount=15&category=21&difficulty={difficulty}&type=multiple")
    print("API Response:", response.text)
    if response.status_code == 200:
        data = response.json()
        if data["response_code"] == 0 and data["results"] != []:
            df = pd.DataFrame(data["results"])
            return df
        else:
            return 0
    elif response.status_code != 200:
        return 0



#Przygotowanie odpowiedzi i pytan
def preload_data(question_index, question_set):
    question = html.unescape(question_set["question"][question_index])
    correct_answer = html.unescape(question_set["correct_answer"][question_index])
    wrong_answers = question_set["incorrect_answers"][question_index]

    print("Question:", question)
    print("Correct Answer:", correct_answer)
    print("Wrong Answers:", wrong_answers)
    #Zastapienie formatowania dla znakow
    # formatting = [
    #     ("#039", "'"),
    #     ("&", "'"),
    #     ("&quot;", '"'),
    #     ("&lt;", "<"),
    #     ("&gt;", ">"),
    # ]

    # #Zastapienie zlych znakow w stringach
    # for tuple in formatting:
    #     question = question.replace(tuple[0], tuple[1])
    #     correct_answer = correct_answer.replace(tuple[0], tuple[1])
    # #Zastapienia zlych znakow w listach
    #     for tuple in formatting:
    #         wrong_answers = [char.replace(tuple[0], tuple[1]) for char in wrong_answers]

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
global parameters
parameters = {
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct": [],
    "score": [],
    "random_question_index": [],
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
    "message": [],
    "message2": [],
    "difficulty-easy": [],
    "difficulty-medium": [],
    "difficulty-hard": [],
}



#Inicjalizacja okna wraz z podstawowymi parametrami i tytułem
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Sport Quiz")
window.setFixedWidth(1000)
window.move(2700, 200)
window.setStyleSheet("background: #4d4c4d;")





#Zainicjalizowanie gridu pod widgety
grid = QGridLayout()



#Stworzenie funkcji, ktora odpowiada za usuwanie widgetow
def clear_widgets():
    for widget_name in widgets:
        if widgets[widget_name] != []:
            widgets[widget_name][-1].hide()
        for _ in range(0, len(widgets[widget_name])):
            widgets[widget_name].pop()


#Stworzenie funkcji, ktora odpowiada za usuwanie parametrow
def clear_parameters():
    for parm in parameters:
        if parameters[parm] != []:
            for _ in range(0, len(parameters[parm])):
                parameters[parm].pop()
    parameters["random_question_index"].append(random.randint(0, 14))
    parameters["score"].append(0)


#Aktualizacja nazwy difficulty
def on_button_click(button):
    button.setStyleSheet(
        "*{border: 4px solid '#292555';" +
        "border-radius: 100px;" +
        "font-size: 20px;" +
        "color: white;" +
        "padding: 5px ;" +
        "margin: 2px 350px;}" +
        "*:hover{background: '#64A314';}" 
        )
    global difficulty
    difficulty = button.text().lower()
    print(difficulty)


#Stworzenie funkcji do pokazania okna startowego(pokazanie pierwszego frame'a)
def show_frame1():
    clear_widgets()
    frame1()


#Stworzenie funkcji do startu gry(pokazanie drugiego frame'a)
def start_game(difficulty_level):
    print(difficulty_level)
    if difficulty_level != "" and difficulty_level != None:
        questions_set = get_question_sets(difficulty_level)
        if type(questions_set) == int:
            print("API NIE DZIALA")
        else:
            clear_widgets()
            clear_parameters()
            preload_data(parameters["random_question_index"][-1], questions_set)
            frame2()
    # Dodaj czasomierz jako pasek postępu




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
        
        #Losowanie kolejnego indexu dla kolejnego pytania
        parameters["random_question_index"].pop()
        parameters["random_question_index"].append(random.randint(0, 14))
        questions_set=get_question_sets(difficulty)
        #Handlowanie bledow wynikajacych z api
        if type(questions_set) == int:
            print("API NIE DZIALA")
        else:
            preload_data(parameters["random_question_index"][-1],questions_set)
            #Aktualizowanie nazw widgetow: question i answery dla kolejnego pytania oraz scorea
            global current_score
            current_score += 10

            widgets["score"][-1].setText(str(current_score))
            widgets["question"][0].setText(parameters["question"][-1])
            for i in range(1, 5):
                widgets[f"answer{i}"][0].setText(str(parameters[f"answer{i}"][-1]))

        if current_score == 20:
            clear_widgets()
            frame3()
    else:
        #Wywolanie kodu po blednej odpowiedzi
        clear_widgets()
        frame4()
        


#Funkcja, ktora generuje strone startowa
def frame1():
    global current_score
    current_score = 0
    clear_widgets()
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
        "margin: 25px 350px;}" +
        "*:hover{background: '#292555';}"
    )
    #Przypisanie funkcji do przycisku
    button.clicked.connect(lambda: start_game(difficulty))
    #Przechowywanie przycisku jako instancji w liście aby miało scope globalny
    widgets["button"].append(button)
    #Dodanie widgetu do grida oraz umieszczenie go w kolumnie 1 i rzędzie 0
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)


    # Dodanie przycisków poziomu trudności
    easy_button = QPushButton("Easy")
    easy_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    easy_button.setStyleSheet(
        "*{border: 4px solid '#292555';" +
        "border-radius: 30px;" +
        "font-size: 20px;" +
        "color: white;" +
        "padding: 5px ;" +
        "margin: 2px 350px;}" +
        "*:hover{background: '#292555';}"
    )
    widgets["difficulty-easy"].append(easy_button)
    grid.addWidget(widgets["difficulty-easy"][-1], 2, 0, 1, 2)
    easy_button.clicked.connect(lambda: on_button_click(easy_button))


    medium_button = QPushButton("Medium")
    medium_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    medium_button.setStyleSheet(
        "*{border: 4px solid '#292555';" +
        "border-radius: 30px;" +
        "font-size: 20px;" +
        "color: white;" +
        "padding: 5px 0;" +
        "margin: 2px 350px;}" +
        "*:hover{background: '#292555';}"
    )
    widgets["difficulty-medium"].append(medium_button)
    grid.addWidget(widgets["difficulty-medium"][-1], 3, 0, 1, 2)
    medium_button.clicked.connect(lambda: on_button_click(medium_button))


    hard_button = QPushButton("Hard")
    hard_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    hard_button.setStyleSheet(
        "*{border: 4px solid '#292555';" +
        "border-radius: 30px;" +
        "font-size: 20px;" +
        "color: white;" +
        "padding: 5px 0;" +
        "margin: 2px 350px;}" +
        "*:hover{background: '#292555';}"
    )
    widgets["difficulty-hard"].append(hard_button) # Dodanie przycisków do słownika widgets
    grid.addWidget(widgets["difficulty-hard"][-1], 4, 0, 1, 2)
    hard_button.clicked.connect(lambda: on_button_click(hard_button))



#Funkcja generujaca druga strone z pytaniem, odpowiedziami i scorem
def frame2():
    #Dodanie widgetu scorea
    global current_score
    
    score = QLabel(str(current_score))
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
    button1 = answer_button(parameters["answer1"][-1], 120, 5)
    button2 = answer_button(parameters["answer2"][-1], 5, 120)
    button3 = answer_button(parameters["answer3"][-1], 120, 5)
    button4 = answer_button(parameters["answer4"][-1], 5, 120)

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



#Stworzenie funckji do wywolania frame'a w przypadku wygranej
def frame3():
    #Widget z gratulacjami
    message = QLabel("Congradulations! You\nare a G!\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti';" +
        "font-size: 25px;" +
        "color: 'white';" +
        "margin: 100px 0px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel(str(current_score))
    score.setStyleSheet(
        "font-size: 100px;" +
        "color: #8FC740;" +
        "margin: 0 75px 0px 75px;" 
        )
    widgets["score"].append(score)

    #Kolejny widget z gratulacjami
    message2 = QLabel("Congratulations you've won the quiz!")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti';" +
        "font-size: 30px;" +
        "color: 'white';" +
        "margin-top:0px;" +
        "margin-bottom:75px;"
        )
    widgets["message2"].append(message2)

    #Stworzenie przycisku i wystylowanie go
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{padding: 25px 0px;" +
        "border: 4px solid '#292555';" +
        "color: 'white';" +
        "font-family: 'Arial';" +
        "font-size: 25px;" +
        "border-radius: 40px;" +
        "margin: 10px 300px;}" +
        "*:hover{background:'#292555';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    #Logo widget
    pixmap = QPixmap('Images/logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px;" +
        "margin-top:75px;" +
        "margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    #Umiejscowienie widgetow na gridzie
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)






def frame4():
    #Wyswietlenie wiadomosci o zakonczeniu gry
    global difficulty
    difficulty=""
    message = QLabel("Sorry, this answer \nwas wrong\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti';" +
        "font-size: 35px;" +
        "color: 'white';" +
        "margin: 75px 5px;" +
        "padding:20px;" 
        )
    widgets["message"].append(message)

    #Widget score'a
    score = QLabel(str(current_score))
    score.setStyleSheet(
        "font-size: 100px;" +
        "color: white;" +
        "margin: 0 75px 0px 75px;"
        )
    widgets["score"].append(score)

  #Dodanie przycisku ponownego startu
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{padding: 25px 0px;" +
        "border: 4px solid '#292555';" +
        "color: 'white';" +
        "font-family: 'Arial';" +
        "font-size: 35px;" +
        "border-radius: 40px;" +
        "margin: 10px 200px;}" +
        "*:hover{background: '#292555';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('Images/sport_quiz_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px;" +
        "margin-top:75px;"
    )
    widgets["logo"].append(logo)

    #Umieszczenie widgetow na gridzie
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)





window.setLayout(grid)
#Zamknięcie okna
window.show()
sys.exit(app.exec())
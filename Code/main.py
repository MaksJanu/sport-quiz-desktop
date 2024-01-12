import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor


#Przechowywanie instancji widgetów w listach
widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
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


def frame1():
    #Wrzucenie grafiki i dostosowanie stylu
    image = QPixmap("Images/logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;")
    #Przechowywanie loga jako instancji w liście aby miało scope globalny
    widgets["logo"].append(logo)
    #Dodanie widgetu do grida oraz umieszczenie go w kolumnie 0 i rzędzie 0
    grid.addWidget(widgets["logo"][-1], 0, 0)

    #Dodanie widgetu przycisku i wystylizowanie go
    button = QPushButton("PLAY")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        "*{border: 4px solid '#4722dd';" +
        "border-radius: 30px;" +
        "font-size: 35px;" +
        "color: white;" +
        "padding: 15px 0;" +
        "margin: 100px 350px;}" +
        "*:hover{background: '#4722dd';}"
    )
    #Przechowywanie przycisku jako instancji w liście aby miało scope globalny
    widgets["button"].append(button)
    #Dodanie widgetu do grida oraz umieszczenie go w kolumnie 1 i rzędzie 0
    grid.addWidget(widgets["button"][-1], 1, 0)



def frame2():
    #Dodanie widgetu scorea
    score = QLabel("80")
    score.setAlignment(QtCore.Qt.AlignCenter)
    score.setStyleSheet(
        "font-size: 35px;" +
        "color: white;" +
        "padding: 20px 15px;" +
        "margin: 200px 20px;" +
        "background: '#64A314';" +
        "border: 1px solid '#64A314';" +
        "border-radius: 40px;"
    )
    widgets["score"].append(score)
    grid.addWidget(widgets["score"][-1], 0, 1)

    #Dodanie widgetu gdzie przechowywane bedzie pytanie
    question = QLabel("Placeholder text will go here!")
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
    grid.addWidget(widgets["question"][-1], 1, 1)








window.setLayout(grid)
#Zamknięcie okna
window.show()
sys.exit(app.exec())
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

#Inicjalizacja okna wraz z podstawowymi parametrami i tytułem
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Sport Quiz")
window.setFixedWidth(1000)
window.move(2700, 200)
window.setStyleSheet("background: #4d4c4d;")
#807f80
#161219
#Zainicjalizowanie gridu pod widgety
grid = QGridLayout()

#Wrzucenie grafiki i dostosowanie stylu
image = QPixmap("Images/logo.png")
logo = QLabel()
logo.setPixmap(image)
logo.setAlignment(QtCore.Qt.AlignCenter)
logo.setStyleSheet("margin-top: 100px;")


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
grid.addWidget(button, 1, 0)




#Dodanie widgetu do grida oraz umieszczenie go w kolumnie 0 i rzędzie 0
grid.addWidget(logo, 0, 0)
window.setLayout(grid)







#Zamknięcie okna
window.show()
sys.exit(app.exec())
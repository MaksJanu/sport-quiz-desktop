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
window.setStyleSheet("background: #161219;")

#Zainicjalizowanie gridu pod widgety
grid = QGridLayout()
#Wrzucenie grafiki
image = QPixmap("Images/logo.png")
logo = QLabel()
logo.setPixmap(image)
#Dodanie widgetu do grida oraz umieszczenie go w kolumnie 0 i rzędzie 0
grid.addWidget(logo, 0, 0)
window.setLayout(grid)

6.29





#Zamknięcie okna
window.show()
sys.exit(app.exec())
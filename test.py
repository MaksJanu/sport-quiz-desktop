import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QTimer

def create_timer_app():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Timer with Loading Bar')
    window.setGeometry(300, 300, 300, 150)

    progress_bar = QProgressBar()
    start_button = QPushButton('Start')

    layout = QVBoxLayout(window)
    layout.addWidget(progress_bar)
    layout.addWidget(start_button)

    return app, window, progress_bar, start_button

def initialize_timer(progress_bar, total_time=10000, timer_interval=100):
    progress_step = 100 / (total_time / timer_interval)

    def start_timer():
        timer.start(timer_interval)

    def update_timer():
        current_value = progress_bar.value()
        if current_value >= 100:
            timer.stop()
            progress_bar.setValue(0)
        else:
            progress_bar.setValue(current_value + progress_step)

    start_button.clicked.connect(start_timer)
    timer = QTimer()
    timer.timeout.connect(update_timer)

    return timer

def run_app(app, window):
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    app, window, progress_bar, start_button = create_timer_app()
    timer = initialize_timer(progress_bar)
    run_app(app, window)

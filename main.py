import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from ui.home import HomePage

def load_stylesheet():
    with open("styles/styles.css", "r") as f:
        return f.read()

def main():
    app = QApplication(sys.argv)
    window_stack = QStackedWidget()
    
    stylesheet = load_stylesheet()
    app.setStyleSheet(stylesheet)

    home_page = HomePage(window_stack)
    window_stack.addWidget(home_page)

    window_stack.setCurrentWidget(home_page)
    window_stack.setWindowTitle("Algorithm Selection")
    window_stack.setGeometry(100, 100, 1000, 800)
    window_stack.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

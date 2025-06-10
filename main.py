import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget, QMainWindow

from ui.home import HomePage

def load_stylesheet():
    with open("styles/styles.css", "r") as f:
        return f.read()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Initialize pages
        self.home_page = HomePage(self.stack)
        self.stack.addWidget(self.home_page)
        
        # Window settings
        self.setWindowTitle("Algorithm Visualizer")
        self.setGeometry(100, 100, 1000, 800)

def main(): 
    app = QApplication(sys.argv)
    
    # Load stylesheet
    stylesheet = load_stylesheet()
    app.setStyleSheet(stylesheet)
    
    # Create and show main window
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 
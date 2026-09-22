import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMenu

class Example(QWidget):
   def __init__(self):
      super().__init__()
      self.initUI()

   def initUI(self):
      btn = QPushButton('Menu', self)
      menu = QMenu(self)
      menu.addAction('Option 1')
      menu.addAction('Option 2')
      btn.setMenu(menu)
      self.setGeometry(300, 300, 300, 200)
      self.setWindowTitle('Menu QPushButton')
      self.show()

def main():
   app = QApplication(sys.argv)
   ex = Example()
   sys.exit(app.exec())

if __name__ == '__main__':
   main()
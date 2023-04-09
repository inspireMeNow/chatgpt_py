from PyQt5 import QtWidgets, QtCore  
from PyQt5.QtGui import QTextCursor  
  
class ChatWindow(QtWidgets.QMainWindow):  
    def __init__(self):  
        super().__init__()  
  
        self.setWindowTitle("ChatGPT")  
        self.resize(400, 500)  
  
        # Create widgets  
        self.messages_list = QtWidgets.QTextEdit(self)  
        self.messages_list.setReadOnly(True)  
  
        self.message_input = QtWidgets.QLineEdit(self)  
        self.send_button = QtWidgets.QPushButton("Send", self)  
        self.send_button.clicked.connect(self.send_message)  
  
        # Create layout  
        central_widget = QtWidgets.QWidget(self)  
        self.setCentralWidget(central_widget)  
  
        layout = QtWidgets.QVBoxLayout()  
        central_widget.setLayout(layout)  
  
        layout.addWidget(self.messages_list)  
        layout.addWidget(self.message_input)  
  
        # Add widgets to layout  
        message_layout = QtWidgets.QHBoxLayout()  
        message_layout.addWidget(self.message_input)  
        message_layout.addWidget(self.send_button)  
        layout.addLayout(message_layout)  
  
    def send_message(self):  
        message = self.message_input.text()  
        self.messages_list.append("You: " + message)  
        self.message_input.clear()  
  
if __name__ == '__main__':  
    app = QtWidgets.QApplication([])  
    window = ChatWindow()  
    window.show()  
    app.exec_()

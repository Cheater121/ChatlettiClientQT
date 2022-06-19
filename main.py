import sys
import datetime
import json
import requests
from PyQt6 import uic, QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    server_adress = "https://chatletti.ru"
    api = "/api/messenger/"

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('untitled.ui', self)
        self.SendButton1.clicked.connect(self.SendButton1_clicked)

    def SendButton1_clicked(self):
        self.sendmessage()

    def sendmessage(self):
        Username = self.Username1.text()
        Messagetext = self.InputText1.text()
        Timestamp = str(datetime.datetime.today())
        Recipient = self.Recipient1.text()
        msg = f"{{\"Username\": \"{Username}\", \"Messagetext\": \"{Messagetext}\", \"Timestamp\": \"{Timestamp}\", \"Recipient\": \"{Recipient}\"}}"
        print(msg)
        url = self.server_adress + self.api + Username
        data = json.loads(msg)
        r = requests.post(url, json=data)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


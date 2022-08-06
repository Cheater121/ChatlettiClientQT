import sys
import datetime
import json
import requests
from PyQt6 import uic, QtWidgets, QtCore


# pyinstaller --add-data "messenger.ui;." --hidden-import=requests --hidden-import=PyQt6 --noconsole main.py
class MainWindow(QtWidgets.QMainWindow):
    host = "https://chatletti.ru"
    path = "/api/messenger"
    rows = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('messenger.ui', self)
        self.SendButton1.clicked.connect(self.SendButton1_clicked)

    def SendButton1_clicked(self):
        self.make_send_show_message()

    # main function - sending message to the server
    def make_send_show_message(self):
        # making message
        username = self.Username1.text()
        messagetext = self.InputText1.text()
        timestamp = str(datetime.datetime.today())
        recipient = self.Recipient1.text()
        msg_dict = f"{{\"Username\": \"{username}\", \"Messagetext\": \"{messagetext}\", \"Timestamp\": \"{timestamp}\", " \
              f"\"Recipient\": \"{recipient}\"}} "
        msg_json = json.loads(msg_dict)
        # sending message
        url = self.host + self.path
        requests.post(url, json=msg_json)
        # showing message to user
        msgtext = f"{username} ({timestamp}): {messagetext}"
        self.listWidget1.insertItem(self.rows, msgtext)
        self.rows += 1

    # main function - getting message from the server
    def getmessage(self):
        username = self.Username1.text()
        url = self.host + self.path + "/" + username
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise AssertionError
        except:
            return None
        else:
            text = response.text
            return text

    def refresh(self):
        answer = self.getmessage()
        if answer != "Not found" and answer is not None:
            answer = json.loads(answer)
            try:
                user_nm = self.Username1.text()
                messages = answer.get(user_nm)
                for msg in messages:
                    username = msg["Username"]
                    messagetext = msg["Messagetext"]
                    timestamp = msg["Timestamp"]
                    msgtext = f"{username} ({timestamp}): {messagetext}"
                    self.listWidget1.insertItem(self.rows, msgtext)
                    self.rows += 1
            except:
                print("Ooops")
                None


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)
    timer.timeout.connect(w.refresh)
    timer.start(5000)
    sys.exit(app.exec())

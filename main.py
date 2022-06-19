import sys
import datetime
import json
import requests
from PyQt6 import uic, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    server_adress = "https://chatletti.ru"
    api = "/api/messenger"
    rows = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('messenger.ui', self)
        self.SendButton1.clicked.connect(self.SendButton1_clicked)
        self.RefreshButton.clicked.connect(self.refresh)

    def SendButton1_clicked(self):
        self.sendmessage()

    def sendmessage(self):
        Username = self.Username1.text()
        Messagetext = self.InputText1.text()
        Timestamp = str(datetime.datetime.today())
        Recipient = self.Recipient1.text()
        msg = f"{{\"Username\": \"{Username}\", \"Messagetext\": \"{Messagetext}\", \"Timestamp\": \"{Timestamp}\", " \
              f"\"Recipient\": \"{Recipient}\"}} "
        url = self.server_adress + self.api
        data = json.loads(msg)
        requests.post(url, json=data)
        msgtext = f"{Username} ({Timestamp}): {Messagetext}"
        self.listWidget1.insertItem(self.rows, msgtext)
        self.rows += 1

    def getmessage(self):
        Username = self.Username1.text()
        url = self.server_adress + self.api + "/" + Username
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise AssertionError
        except AssertionError:
            return None
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
                UserNM = self.Username1.text()
                messages = answer.get(UserNM)
                for msg in messages:
                    Username = msg["Username"]
                    Messagetext = msg["Messagetext"]
                    Timestamp = msg["Timestamp"]
                    msgtext = f"{Username} ({Timestamp}): {Messagetext}"
                    self.listWidget1.insertItem(self.rows, msgtext)
                    self.rows += 1
            except:
                print("Ooops")
                None


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


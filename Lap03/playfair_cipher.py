import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Đảm bảo file ui/playfair.py tồn tại và có class Ui_MainWindow
from ui.playfair import Ui_MainWindow 
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối sự kiện Click
        self.ui.encrypt_button.clicked.connect(self.call_api_encrypt)
        self.ui.decrypt_button.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        payload = {
            "plain_text": self.ui.Plain_text.toPlainText(),
            "key": self.ui.Key.toPlainText()
        }
        try:
            # Sửa json-payload thành json=payload
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.Cipher_text.setPlainText(data["encrypted_message"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.setWindowTitle("Thông báo")
                msg.exec_()
            else:
                print(f"Error while calling API: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        payload = {
            "cipher_text": self.ui.Cipher_text.toPlainText(),
            "key": self.ui.Key.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.Plain_text.setPlainText(data["decrypted_message"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.setWindowTitle("Thông báo")
                msg.exec_()
            else:
                print(f"Error while calling API: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
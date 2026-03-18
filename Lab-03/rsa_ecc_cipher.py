import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Import class giao diện từ file ecc-rsa.py của bạn
from ui.ecc_rsa import Ui_MainWindow 

class CipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # --- KẾT NỐI EVENT CHO RSA ---
        self.ui.btn_gen_keys.clicked.connect(self.call_api_rsa_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_rsa_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_rsa_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_rsa_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_rsa_verify)

        # --- KẾT NỐI EVENT CHO ECC ---
        # Lưu ý: btn_sign_2 và btn_verify_2 trong UI của bạn đang để text là "ECC"
        self.ui.btn_sign_2.clicked.connect(self.call_api_ecc_sign)
        self.ui.btn_verify_2.clicked.connect(self.call_api_ecc_verify)

    # --- LOGIC RSA ---
    def call_api_rsa_gen_keys(self):
        # Gen keys cho cả RSA và ECC
        rsa_url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        ecc_url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        try:
            rsa_response = requests.get(rsa_url)
            ecc_response = requests.get(ecc_url)
            if rsa_response.status_code == 200 and ecc_response.status_code == 200:
                QMessageBox.information(self, "Thông báo", "Keys generated for RSA and ECC")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể kết nối API: {str(e)}")

    def call_api_rsa_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {"message": self.ui.txt_plain_text.toPlainText(), "key_type": "public"}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.ui.txt_cipher_text.setText(response.json()["encrypted_message"])
                QMessageBox.information(self, "Thành công", "Đã mã hóa RSA")
        except Exception as e:
            print(e)

    def call_api_rsa_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {"ciphertext": self.ui.txt_cipher_text.toPlainText(), "key_type": "private"}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.ui.txt_plain_text.setText(response.json()["decrypted_message"])
                QMessageBox.information(self, "Thành công", "Đã giải mã RSA")
        except Exception as e:
            print(e)

    def call_api_rsa_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {"message": self.ui.txt_info.toPlainText()}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.ui.txt_sign.setText(response.json()["signature"])
                QMessageBox.information(self, "RSA", "Đã ký số thành công")
        except Exception as e:
            print(e)

    def call_api_rsa_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                valid = response.json()["is_verified"]
                msg = "Chữ ký RSA Hợp lệ!" if valid else "Chữ ký RSA Không hợp lệ!"
                QMessageBox.information(self, "Kết quả xác minh", msg)
        except Exception as e:
            print(e)

    # --- LOGIC ECC ---
    def call_api_ecc_sign(self):
        url = "http://127.0.0.1:5000/api/ecc/sign"
        payload = {"message": self.ui.txt_info_2.toPlainText()}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    QMessageBox.critical(self, "Lỗi", f"Lỗi sign: {data['error']}")
                else:
                    self.ui.txt_sign_2.setText(data["signature"])
                    QMessageBox.information(self, "ECC", "Đã ký số ECC thành công")
            else:
                QMessageBox.critical(self, "Lỗi", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể kết nối API: {str(e)}")

    def call_api_ecc_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"
        payload = {
            "message": self.ui.txt_info_2.toPlainText(),
            "signature": self.ui.txt_sign_2.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if 'error' in data:
                    QMessageBox.critical(self, "Lỗi", f"Lỗi verify: {data['error']}")
                else:
                    valid = data["is_verified"]
                    msg = "Chữ ký ECC Hợp lệ!" if valid else "Chữ ký ECC Không hợp lệ!"
                    QMessageBox.information(self, "Kết quả xác minh", msg)
            else:
                QMessageBox.critical(self, "Lỗi", f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể kết nối API: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CipherApp()
    window.show()
    sys.exit(app.exec_())
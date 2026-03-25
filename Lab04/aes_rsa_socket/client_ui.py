import tkinter as tk
from tkinter import scrolledtext, messagebox
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import socket
import threading

class SecureChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Chat Client (RSA + AES)")
        self.root.geometry("400x500")
        
        # --- THIẾT KẾ GIAO DIỆN ---
        # Khung hiển thị tin nhắn
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', font=("Arial", 10))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Khung nhập liệu
        input_frame = tk.Frame(root)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        self.msg_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.msg_entry.bind("<Return>", self.send_message) # Nhấn Enter để gửi
        
        self.send_btn = tk.Button(input_frame, text="Gửi", command=self.send_message, bg="#0078D7", fg="white", font=("Arial", 10, "bold"))
        self.send_btn.pack(side=tk.RIGHT)

        # --- KHỞI TẠO MẠNG VÀ BẢO MẬT ---
        self.aes_key = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.client_socket.connect(('localhost', 12345))
            self.setup_security()
            
            # Chạy luồng nhận tin nhắn
            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()
            self.display_message("Hệ thống: Đã kết nối và thiết lập mã hóa bảo mật thành công!")
            
        except ConnectionRefusedError:
            messagebox.showerror("Lỗi", "Không thể kết nối đến server. Hãy chắc chắn server.py đang chạy.")
            self.root.destroy()

        # Xử lý khi tắt cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_security(self):
        """Khởi tạo trao đổi khóa RSA và nhận khóa AES từ server"""
        client_key = RSA.generate(2048)
        
        # Nhận public key của server và gửi public key của mình
        server_public_key = RSA.import_key(self.client_socket.recv(2048))
        self.client_socket.send(client_key.publickey().export_key(format='PEM'))
        
        # Nhận khóa AES đã mã hóa bằng public key của client và giải mã nó
        encrypted_aes_key = self.client_socket.recv(2048)
        cipher_rsa = PKCS1_OAEP.new(client_key)
        self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)

    def encrypt_message(self, key, message):
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ciphertext

    def decrypt_message(self, key, encrypted_message):
        iv = encrypted_message[:AES.block_size]
        ciphertext = encrypted_message[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_message.decode()

    def display_message(self, message):
        """Hiển thị tin nhắn lên màn hình một cách an toàn (thread-safe)"""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.yview(tk.END) # Tự động cuộn xuống cuối
        self.chat_area.config(state='disabled')

    def send_message(self, event=None):
        message = self.msg_entry.get().strip()
        if message:
            # Hiển thị lên màn hình mình
            self.display_message(f"Bạn: {message}")
            self.msg_entry.delete(0, tk.END)
            
            # Mã hóa và gửi đi
            try:
                encrypted_message = self.encrypt_message(self.aes_key, message)
                self.client_socket.send(encrypted_message)
                
                if message.lower() == "exit":
                    self.on_closing()
            except Exception as e:
                self.display_message(f"Lỗi khi gửi: {e}")

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if not encrypted_message:
                    break
                decrypted_message = self.decrypt_message(self.aes_key, encrypted_message)
                
                # Cập nhật UI từ luồng background cần thông qua root.after (đảm bảo an toàn cho Tkinter)
                self.root.after(0, self.display_message, f"Đối tác: {decrypted_message}")
            except OSError:
                break # Bắt lỗi khi socket bị đóng
            except Exception as e:
                print(f"Lỗi nhận tin nhắn: {e}")
                break

    def on_closing(self):
        try:
            # Báo cho server biết mình thoát
            if self.aes_key:
                exit_msg = self.encrypt_message(self.aes_key, "exit")
                self.client_socket.send(exit_msg)
            self.client_socket.close()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureChatApp(root)
    root.mainloop()
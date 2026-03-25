import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import os

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

class DiffieHellmanUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Diffie-Hellman Key Exchange UI")
        self.root.geometry("550x500")
        
        # --- KHUNG SERVER ---
        server_frame = tk.LabelFrame(root, text=" 1. Server Side ", font=("Arial", 10, "bold"))
        server_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.btn_server = tk.Button(server_frame, text="Khởi tạo Server (Tạo tham số & Public Key)", 
                                    command=self.run_server_thread, bg="#4CAF50", fg="white")
        self.btn_server.pack(pady=5)
        
        self.server_log = scrolledtext.ScrolledText(server_frame, height=6, wrap=tk.WORD)
        self.server_log.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # --- KHUNG CLIENT ---
        client_frame = tk.LabelFrame(root, text=" 2. Client Side ", font=("Arial", 10, "bold"))
        client_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.btn_client = tk.Button(client_frame, text="Khởi tạo Client (Sinh Shared Secret)", 
                                    command=self.run_client, bg="#2196F3", fg="white", state=tk.DISABLED)
        self.btn_client.pack(pady=5)
        
        self.client_log = scrolledtext.ScrolledText(client_frame, height=6, wrap=tk.WORD)
        self.client_log.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def log_server(self, msg):
        self.server_log.insert(tk.END, msg + "\n")
        self.server_log.yview(tk.END)

    def log_client(self, msg):
        self.client_log.insert(tk.END, msg + "\n")
        self.client_log.yview(tk.END)

    # --- LOGIC SERVER ---
    def run_server_thread(self):
        self.btn_server.config(state=tk.DISABLED)
        self.log_server("Đang tạo tham số DH (2048-bit)... Vui lòng đợi vài giây...")
        # Chạy thread để không làm đơ UI
        threading.Thread(target=self.generate_server_keys, daemon=True).start()

    def generate_server_keys(self):
        try:
            # Code từ server.py
            parameters = dh.generate_parameters(generator=2, key_size=2048)
            private_key = parameters.generate_private_key()
            public_key = private_key.public_key()
            
            # Lưu file PEM
            with open("server_public_key.pem", "wb") as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM, 
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
            
            # Cập nhật UI an toàn từ thread phụ
            self.root.after(0, self.log_server, "Đã tạo xong private/public key cho Server!")
            self.root.after(0, self.log_server, "Đã lưu Public Key vào 'server_public_key.pem'.")
            
            # Bật nút Client
            self.root.after(0, lambda: self.btn_client.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_server.config(state=tk.NORMAL))
            
        except Exception as e:
            self.root.after(0, self.log_server, f"Lỗi Server: {str(e)}")
            self.root.after(0, lambda: self.btn_server.config(state=tk.NORMAL))

    # --- LOGIC CLIENT ---
    def run_client(self):
        if not os.path.exists("server_public_key.pem"):
            messagebox.showerror("Lỗi", "Không tìm thấy server_public_key.pem. Hãy chạy Server trước!")
            return
            
        self.log_client("Đang đọc Public Key của Server...")
        try:
            # Code từ client.py
            with open("server_public_key.pem", "rb") as f:
                server_public_key = serialization.load_pem_public_key(f.read())
                
            parameters = server_public_key.parameters()
            private_key = parameters.generate_private_key()
            
            self.log_client("Đang tính toán Shared Secret...")
            shared_secret = private_key.exchange(server_public_key)
            
            self.log_client("Hoàn tất! Shared Secret của Client (Hex):")
            self.log_client(shared_secret.hex())
            
        except Exception as e:
            self.log_client(f"Lỗi Client: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiffieHellmanUI(root)
    root.mainloop()
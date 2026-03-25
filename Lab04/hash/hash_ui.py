import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from Crypto.Hash import SHA3_256

def blake2_hash(message_bytes):
    blake2_h = hashlib.blake2b(digest_size=64)
    blake2_h.update(message_bytes)
    return blake2_h.hexdigest()

def lib_md5(message_bytes):
    md5_h = hashlib.md5()
    md5_h.update(message_bytes)
    return md5_h.hexdigest()

def sha3_hash(message_bytes):
    sha3_h = SHA3_256.new()
    sha3_h.update(message_bytes)
    return sha3_h.hexdigest()

def sha256_hash(message_bytes):
    sha256_h = hashlib.sha256()
    sha256_h.update(message_bytes)
    return sha256_h.hexdigest()

class HashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Công cụ Băm Văn Bản (Hash Generator)")
        self.root.geometry("550x300")
        self.root.resizable(False, False)

        # Dictionary lưu trữ hàm tương ứng với tên thuật toán
        self.algorithms = {
            "BLAKE2b": blake2_hash,
            "MD5": lib_md5,
            "SHA-3": sha3_hash,
            "SHA-256": sha256_hash
        }

        self.create_widgets()

    def create_widgets(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Nhập chuỗi văn bản
        ttk.Label(main_frame, text="Nhập chuỗi văn bản:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.input_entry = ttk.Entry(main_frame, width=60)
        self.input_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # 2. Chọn thuật toán
        ttk.Label(main_frame, text="Chọn thuật toán băm:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.algo_combobox = ttk.Combobox(main_frame, values=list(self.algorithms.keys()), state="readonly", width=30)
        self.algo_combobox.current(3) # Mặc định chọn SHA-256
        self.algo_combobox.grid(row=3, column=0, sticky=tk.W, pady=(0, 15))

        # 3. Nút Thực hiện băm
        self.hash_btn = ttk.Button(main_frame, text="Tạo mã băm", command=self.generate_hash)
        self.hash_btn.grid(row=3, column=1, sticky=tk.W, padx=10, pady=(0, 15))

        # 4. Kết quả Output
        ttk.Label(main_frame, text="Kết quả (Mã băm):").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.output_entry = ttk.Entry(main_frame, width=60, state="readonly")
        self.output_entry.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # 5. Nút Copy (tiện ích bổ sung)
        self.copy_btn = ttk.Button(main_frame, text="Sao chép kết quả", command=self.copy_to_clipboard)
        self.copy_btn.grid(row=6, column=0, sticky=tk.W)

    def generate_hash(self):
        # Lấy văn bản từ input
        text = self.input_entry.get()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập chuỗi cần băm!")
            return

        # Encode văn bản sang utf-8
        message_bytes = text.encode('utf-8')
        
        # Lấy thuật toán được chọn
        selected_algo = self.algo_combobox.get()
        hash_function = self.algorithms[selected_algo]

        try:
            # Thực hiện băm
            hashed_result = hash_function(message_bytes)
            
            # Cập nhật kết quả lên UI
            self.output_entry.config(state="normal")
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, hashed_result)
            self.output_entry.config(state="readonly")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã có lỗi xảy ra: {str(e)}")

    def copy_to_clipboard(self):
        result = self.output_entry.get()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Thành công", "Đã sao chép mã băm vào khay nhớ tạm!")
        else:
            messagebox.showwarning("Cảnh báo", "Chưa có kết quả để sao chép.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HashApp(root)
    root.mainloop()
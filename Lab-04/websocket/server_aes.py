import tornado.ioloop
import tornado.web
import tornado.websocket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

# Định nghĩa khoá AES 16 bytes (128-bit)
AES_KEY = b'MySecretKey12345'

class WebSocketServer(tornado.websocket.WebSocketHandler):
    # Hàm này chạy khi có client kết nối tới
    def open(self):
        print("Mới có Client kết nối tới Server.")

    # Hàm này chạy khi client ngắt kết nối
    def on_close(self):
        print("Client đã ngắt kết nối.")

    # Hàm này nhận thông điệp từ client, mã hoá và gửi lại
    def on_message(self, message):
        print(f"Nhận được từ client: {message}")
        
        try:
            # 1. Khởi tạo đối tượng mã hoá AES chế độ CBC
            cipher = AES.new(AES_KEY, AES.MODE_CBC)
            
            # 2. Đệm (pad) dữ liệu và mã hoá
            ct_bytes = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
            
            # 3. Chuyển đổi IV và CipherText sang chuỗi Base64 để dễ đọc/gửi qua mạng
            iv = base64.b64encode(cipher.iv).decode('utf-8')
            ct = base64.b64encode(ct_bytes).decode('utf-8')
            
            encrypted_message = f"IV:{iv} | CipherText:{ct}"
            
            print("-> Đã mã hoá và gửi trả lại client.")
            self.write_message(encrypted_message)
            
        except Exception as e:
            error_msg = f"Lỗi mã hoá: {str(e)}"
            print(error_msg)
            self.write_message(error_msg)

def main():
    app = tornado.web.Application([
        (r"/websocket/", WebSocketServer)
    ], websocket_ping_interval=10, websocket_ping_timeout=30)
    
    app.listen(8888)
    print("Server đang lắng nghe tại ws://localhost:8888/websocket/ ...")
    
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.start()

if __name__ == "__main__":
    main()
import tornado.ioloop
import tornado.websocket
import threading
import time

class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop

    def start(self):
        self.connect_and_read()

    def stop(self):
        self.io_loop.stop()

    def connect_and_read(self):
        print("Đang kết nối đến Server...")
        tornado.websocket.websocket_connect(
            url="ws://localhost:8888/websocket/", 
            callback=self.maybe_retry_connection, 
            on_message_callback=self.on_message,
        )

    def maybe_retry_connection(self, future) -> None:
        try:
            self.connection = future.result()
            print("✅ Đã kết nối thành công tới Server!")
            
            # Sử dụng Thread riêng để nhập liệu không làm treo luồng chính (IOLoop)
            input_thread = threading.Thread(target=self.read_input_from_console)
            input_thread.daemon = True # Tự động đóng thread khi thoát chương trình
            input_thread.start()
            
        except Exception as e:
            print(f"Không thể kết nối ({e}), đang thử lại sau 3 giây...")
            self.io_loop.call_later(3, self.connect_and_read)

    def on_message(self, message):
        if message is None:
            print("\n❌ Bị mất kết nối với Server, đang kết nối lại...")
            self.connection = None
            self.connect_and_read()
            return
            
        print(f"\n[Mã hoá AES từ Server] {message}")

    def read_input_from_console(self):
        # Đợi 1 chút để log "kết nối thành công" kịp in ra
        time.sleep(0.5) 
        while True:
            try:
                # Lệnh input() nằm ở luồng riêng nên an toàn trên Windows
                message = input("\nNhập thông điệp gửi Server: ")
                if self.connection and message.strip():
                    # Đưa lệnh gửi message vào hàng đợi của luồng chính một cách an toàn
                    self.io_loop.add_callback(self.connection.write_message, message)
            except Exception as e:
                break

def main():
    # Khởi tạo IOLoop
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    
    # Đăng ký chạy client
    io_loop.add_callback(client.start)
    
    try:
        # Bắt đầu vòng lặp vô hạn để giữ chương trình chạy
        io_loop.start()
    except KeyboardInterrupt:
        print("\nĐang thoát chương trình...")
        client.stop()

# QUAN TRỌNG: Phải có đoạn này để gọi hàm main() khởi động chương trình
if __name__ == "__main__":
    main()
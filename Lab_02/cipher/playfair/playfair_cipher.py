class PlayfairCipher:
    def __init__(self, key: str | None = None):

        self.key = key
        self.matrix = self.create_playfair_matrix(key) if key else None

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I")  # Chuyển "J" thành "I" trong khóa
        key = key.upper()
        key_set = set(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [letter for letter in alphabet if letter not in key_set]
        matrix = list(key)
        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col

    def encrypt_text(self, plain_text):
        if not self.matrix:
            raise ValueError("Playfair matrix not initialized. Provide a key when constructing the cipher.")
        # Chuyển "J" thành "I" trong văn bản đầu vào
        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.upper()
        encrypted_text = ""
        for i in range(0, len(plain_text), 2):
            pair = plain_text[i:i+2]
            if len(pair) == 1:  # Xử lý nếu số lượng ký tự lẻ
                pair += "X"
            row1, col1 = self.find_letter_coords(self.matrix, pair[0])
            row2, col2 = self.find_letter_coords(self.matrix, pair[1])
            if row1 == row2:
                encrypted_text += self.matrix[row1][((col1 + 1) % 5)] + self.matrix[row2][((col2 + 1) % 5)]
            elif col1 == col2:
                encrypted_text += self.matrix[((row1 + 1) % 5)][col1] + self.matrix[((row2 + 1) % 5)][col2]
            else:
                encrypted_text += self.matrix[row1][col2] + self.matrix[row2][col1]
        return encrypted_text
    def decrypt_text(self, cipher_text):
        if not self.matrix:
            raise ValueError("Playfair matrix not initialized. Provide a key when constructing the cipher.")
        cipher_text = cipher_text.upper()
        decrypted_text = ""
        decrypted_text1 = ""
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(self.matrix, pair[0])
            row2, col2 = self.find_letter_coords(self.matrix, pair[1])
            if row1 == row2:
                decrypted_text += self.matrix[row1][((col1 - 1) % 5)] + self.matrix[row2][((col2 - 1) % 5)]
            elif col1 == col2:
                decrypted_text += self.matrix[((row1 - 1) % 5)][col1] + self.matrix[((row2 - 1) % 5)][col2]
            else:
                decrypted_text += self.matrix[row1][col2] + self.matrix[row2][col1]
        banro = ""
        # Loại bỏ ký tự 'X' nếu nó là ký tự cuối cùng và là ký tự được thêm
        # vào
        for i in range(0, len(decrypted_text)-2, 2):
            if decrypted_text[i] == decrypted_text[i+2]:
                banro += decrypted_text[i]
            else:
                banro += decrypted_text[i] + decrypted_text[i+1]
        if decrypted_text[-1] == "X":
            banro += decrypted_text[-2]
        else:
            banro += decrypted_text[-2] + decrypted_text[-1]
        return banro
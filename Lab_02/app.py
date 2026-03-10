from flask import Flask, render_template, request, json
from cipher.caesar import CaesarCipher
from cipher.playfair import PlayfairCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# CAESAR CIPHER
@app.route("/caesar")
def caesar():
    return render_template("caesar.html")

@app.route("/encrypt", methods=["POST"])
def caesar_encrypt():
    plain_text = request.form["inputPlainText"]
    key = int(request.form["inputKeyPlain"])
    caesar_cipher = CaesarCipher()
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return f"text: {plain_text} <br/> key: {key} <br/> encrypted text: {encrypted_text}"

@app.route("/decrypt", methods=["POST"])
def caesar_decrypt():
    cipher_text = request.form["inputCipherText"]
    key = int(request.form["inputKeyCipher"])
    caesar_cipher = CaesarCipher()
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return f"text: {cipher_text} <br/> key: {key} <br/> decrypted text: {decrypted_text}"

# PLAYFAIR CIPHER
@app.route("/playfair")
def playfair():
    return render_template("playfair.html")

@app.route("/playfair_encrypt", methods=["POST"])
def playfair_encrypt():
    plain_text = request.form["inputPlainText"]
    key = request.form["inputKeyPlain"]
    playfair_cipher = PlayfairCipher(key)
    encrypted_text = playfair_cipher.encrypt_text(plain_text)
    return f"text: {plain_text} <br/> key: {key} <br/> encrypted text: {encrypted_text}"

@app.route("/playfair_decrypt", methods=["POST"])
def playfair_decrypt():
    cipher_text = request.form["inputCipherText"]
    key = request.form["inputKeyCipher"]
    playfair_cipher = PlayfairCipher(key)
    decrypted_text = playfair_cipher.decrypt_text(cipher_text)
    return f"text: {cipher_text} <br/> key: {key} <br/> decrypted text: {decrypted_text}"

# VIGENÈRE CIPHER
@app.route("/vigenere")
def vigenere():
    return render_template("vigenere.html")

@app.route("/vigenere_encrypt", methods=["POST"])
def vigenere_encrypt():
    plain_text = request.form["inputPlainText"]
    key = request.form["inputKeyPlain"]
    vigenere_cipher = VigenereCipher()
    encrypted_text = vigenere_cipher.encrypt_text(plain_text, key)
    return f"text: {plain_text} <br/> key: {key} <br/> encrypted text: {encrypted_text}"

@app.route("/vigenere_decrypt", methods=["POST"])
def vigenere_decrypt():
    cipher_text = request.form["inputCipherText"]
    key = request.form["inputKeyCipher"]
    vigenere_cipher = VigenereCipher()
    decrypted_text = vigenere_cipher.decrypt_text(cipher_text, key)
    return f"text: {cipher_text} <br/> key: {key} <br/> decrypted text: {decrypted_text}"

# RAIL FENCE CIPHER
@app.route("/railfence")
def railfence():
    return render_template("railfence.html")

@app.route("/railfence_encrypt", methods=["POST"])
def railfence_encrypt():
    plain_text = request.form["inputPlainText"]
    rails = int(request.form["inputKeyPlain"])
    railfence_cipher = RailFenceCipher()
    encrypted_text = railfence_cipher.encrypt_text(plain_text, rails)
    return f"text: {plain_text} <br/> rails: {rails} <br/> encrypted text: {encrypted_text}"

@app.route("/railfence_decrypt", methods=["POST"])
def railfence_decrypt():
    cipher_text = request.form["inputCipherText"]
    rails = int(request.form["inputKeyCipher"])
    railfence_cipher = RailFenceCipher()
    decrypted_text = railfence_cipher.decrypt_text(cipher_text, rails)
    return f"text: {cipher_text} <br/> rails: {rails} <br/> decrypted text: {decrypted_text}"

# TRANSPOSITION CIPHER
@app.route("/transposition")
def transposition():
    return render_template("transposition.html")

@app.route("/transposition_encrypt", methods=["POST"])
def transposition_encrypt():
    plain_text = request.form["inputPlainText"]
    key = request.form["inputKeyPlain"]
    transposition_cipher = TranspositionCipher()
    encrypted_text = transposition_cipher.encrypt_text(plain_text, key)
    return f"text: {plain_text} <br/> key: {key} <br/> encrypted text: {encrypted_text}"

@app.route("/transposition_decrypt", methods=["POST"])
def transposition_decrypt():
    cipher_text = request.form["inputCipherText"]
    key = request.form["inputKeyCipher"]
    transposition_cipher = TranspositionCipher()
    decrypted_text = transposition_cipher.decrypt_text(cipher_text, key)
    return f"text: {cipher_text} <br/> key: {key} <br/> decrypted text: {decrypted_text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
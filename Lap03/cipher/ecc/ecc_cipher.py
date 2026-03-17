import ecdsa, os

if not os.path.exists('cipher/ecc/keys'):
    os.makedirs('cipher/ecc/keys')

class ECCCipher:
    def __init__(self):
        pass

    def generate_keys(self):
        sk = ecdsa.SigningKey.generate()
        vk = sk.get_verifying_key()

        # Tạo khóa riêng tư
        # Lấy khóa công khai từ khóa riêng
        with open('cipher/ecc/keys/privateKey.pem', 'wb') as p:
            p.write(sk.to_pem())
        with open('cipher/ecc/keys/publickey.pem', 'wb') as p:
            p.write(vk.to_pem())

    def load_keys(self):
        with open('cipher/ecc/keys/privatekey.pem', 'rb') as p:
            sk = ecdsa.SigningKey.from_pem(p.read())
        with open('cipher/ecc/keys/publickey.pem', 'rb') as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())
        return sk, vk

    def sign(self, message, key):
        # Ký dữ liệu bằng khóa riêng tư
        return key.sign(message.encode('utf-8'))

    def verify(self, message, signature, key):
        try:
            return key.verify(signature, message.encode('utf-8'))
        except ecdsa.BadSignatureError:
            return False
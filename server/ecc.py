from tinyec import registry, ec
from Crypto.Cipher import ChaCha20_Poly1305
import secrets
import hashlib, binascii

def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y % 2)[2:]

class Ecc():
    def __init__(self) -> None:
        self.curve = registry.get_curve('brainpoolP256r1')

    # @staticmethod
    # def generate_curve():
    #     return registry.get_curve('brainpoolP256r1')

    def generate_priv_key(self) -> int:
        return secrets.randbelow(self.curve.field.n)

    def calculate_pub_key(self, priv_key: int):
        return priv_key * self.curve.g
    
    def encrypt_aed(self, msg, secret):
        header = b'header'
        cipher = ChaCha20_Poly1305.new(key=secret)
        cipher.update(header)
        ciphertext, tag = cipher.encrypt_and_digest(msg)
        return (ciphertext, cipher.nonce, header, tag)

    def decrypt_aed(self, ciphertext, nonce, tag, secret):
        try:
            header = b'header'
            cipher = ChaCha20_Poly1305.new(key=secret, nonce=nonce)
            cipher.update(header)
            plaintext = cipher.decrypt_and_verify(ciphertext=ciphertext, received_mac_tag=tag)
            print(plaintext)
            return plaintext
        except (ValueError, KeyError):
            return 

    def ecc_point_to_256_bit_key(self, point):
        sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
        sha.update(int.to_bytes(point.y, 32, 'big'))
        return sha.digest()

    def encrypt(self, msg, pub_key):
        priv_key = self.generate_priv_key()
        shared_secret = priv_key*pub_key
        shared_secret_key = self.ecc_point_to_256_bit_key(shared_secret)
        ciphertext, nonce, header, tag = self.encrypt_aed(msg, shared_secret_key)
        pub_key = self.calculate_pub_key(priv_key=priv_key)
        return (ciphertext, nonce, tag, pub_key)

    def decrypt(self, ecrypted_msg, priv_key):
        (ciphertext, nonce, tag, pub_key) = ecrypted_msg
        shared_secret = priv_key * pub_key
        shared_secret_key = self.ecc_point_to_256_bit_key(shared_secret)
        plaintext = self.decrypt_aed(ciphertext=ciphertext, nonce=nonce, tag=tag, secret=shared_secret_key)
        return plaintext

if __name__ == "__main__":
    curve = Ecc()

    # alicePrivKey = curve.generate_priv_key()
    # alicePubKey = curve.calculate_pub_key(alicePrivKey)
    # print("Alice public key:", compress(alicePubKey))

    # bobPrivKey = curve.generate_priv_key()
    # bobPubKey = curve.calculate_pub_key(bobPrivKey)
    # print("Bob public key:", compress(bobPubKey))

    # aliceSharedKey = alicePrivKey * bobPubKey
    # print("Alice shared key:", compress(aliceSharedKey))

    # bobSharedKey = bobPrivKey * alicePubKey
    # print("Bob shared key:", compress(bobSharedKey))

    # print("Equal shared keys:", aliceSharedKey == bobSharedKey)

    msg = b'Text to be encrypted by ECC public key and ' \
        b'decrypted by its corresponding ECC private key'
    print("original msg:", msg)
    privKey = curve.generate_priv_key()
    pubKey = curve.calculate_pub_key(priv_key=privKey)

    encryptedMsg = curve.encrypt(msg, pubKey)
    encryptedMsgObj = {
        'ciphertext': binascii.hexlify(encryptedMsg[0]),
        'nonce': binascii.hexlify(encryptedMsg[1]),
        'authTag': binascii.hexlify(encryptedMsg[2]),
        'ciphertextPubKey': hex(encryptedMsg[3].x) + hex(encryptedMsg[3].y % 2)[2:]
    }
    print("encrypted msg:", encryptedMsgObj)

    decryptedMsg = curve.decrypt(encryptedMsg, priv_key=privKey)
    print("decrypted msg:", decryptedMsg)
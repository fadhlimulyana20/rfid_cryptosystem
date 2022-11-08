from tinyec import registry, ec
import secrets

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

curve = Ecc()

alicePrivKey = curve.generate_priv_key()
alicePubKey = curve.calculate_pub_key(alicePrivKey)
print("Alice public key:", compress(alicePubKey))

bobPrivKey = curve.generate_priv_key()
bobPubKey = curve.calculate_pub_key(bobPrivKey)
print("Bob public key:", compress(bobPubKey))

aliceSharedKey = alicePrivKey * bobPubKey
print("Alice shared key:", compress(aliceSharedKey))

bobSharedKey = bobPrivKey * alicePubKey
print("Bob shared key:", compress(bobSharedKey))

print("Equal shared keys:", aliceSharedKey == bobSharedKey)
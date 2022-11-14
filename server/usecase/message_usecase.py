from pymongo.database import Database
from repositories.message_repo import MessageRepository
from models.message import MessageRequest, MessageEncryptedData, MessageDecryptData
from utils.ecc import Ecc
from tinyec import registry
import hashlib

class MessageUsecase():
    message_repo: MessageRepository
    def __init__(self, db: Database) -> None:
        self.message_repo = MessageRepository(db)
    
    def encrypt_message(self, data: MessageRequest):
        # TODO : add function to encrypt message with ECC algorithm
        ecc = Ecc()
        reader_priv_key = ecc.generate_priv_key()
        reader_pub_key = ecc.calculate_pub_key(reader_priv_key)
        msg = bytes(data.msg, 'utf-8')
        encrypted_msg = ecc.encrypt(msg, reader_pub_key)
        print(encrypted_msg)
        data_to_be_stored = MessageEncryptedData(
            g_curve={
                'name': ecc.curve.name,
                'a': str(ecc.curve.a),
                'b': str(ecc.curve.b),
                'field': {
                    'p': str(ecc.curve.field.p),
                    'g': str(ecc.curve.field.g),
                    'n': str(ecc.curve.field.n),
                    'h': str(ecc.curve.field.h)
                }
            },
            priv_key_reader=str(reader_priv_key),
            priv_key_tag=str(encrypted_msg[4]),
            plaintext=data.msg,
            nonce=encrypted_msg[1]
        )
        result = self.message_repo.add_message(data_to_be_stored)
        return result

    def create_ecc(self, a, b, field, name):
        ecc = Ecc()
        ecc.custom_curve(a, b, field, name)
        return ecc

    def decrypt_message(self, data: MessageDecryptData):
        cur = self.message_repo.get_all_message()
        msg = None
        pub_key_tag = None
        ecc = None
        for c in cur:
            priv_key_tag = int(c['priv_key_tag'])
            a = int(c['g_curve']['a'])
            b = int(c['g_curve']['b'])
            name = c['g_curve']['name']
            field = registry.ec.SubGroup(
                p=int(c['g_curve']['field']['p']),
                g=int(c['g_curve']['field']['g']),
                n=int(c['g_curve']['field']['n']),
                h=int(c['g_curve']['field']['h'])
            )
            ecc = self.create_ecc(a, b, field, name)
            pub_key_tag = ecc.calculate_pub_key(priv_key_tag)
            pub_key_tag_str = str(pub_key_tag.x) + str(pub_key_tag.y) + str(pub_key_tag.p)
            pub_key_tag_hashed = hashlib.sha256(pub_key_tag_str.encode('utf-8')).hexdigest()
            if (data.hashed_pub_key == pub_key_tag_hashed):
                msg = c
                break
        if (msg is not None):
            #Decrypt Here
            priv_key_reader = int(c['priv_key_reader'])
            enctypted_msg = (
                data.ciphertext.encode('utf-8'),
                data.nonce,
                pub_key_tag,
                int(c['priv_key_tag'])
            )
            decypted_msg = ecc.decrypt(ecrypted_msg=enctypted_msg, priv_key=priv_key_reader)
            # Check whether plaintext and plaintext in DB are the same

            return decypted_msg


from database.database import get_database
from models.message import MessageRequest   

if __name__ == "__main__":
    db = get_database()
    data = MessageRequest(
        msg="Test",
        algorithm="ecc",
        type="encrypt"
    )
    mu = MessageUsecase(db)
    res = mu.encrypt_message(data)
    print(res)
    assert res
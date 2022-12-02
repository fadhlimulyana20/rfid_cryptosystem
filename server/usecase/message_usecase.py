from pymongo.database import Database
from repositories.message_repo import MessageRepository
from models.message import MessageRequest, MessageEncryptedData, MessageDecryptData
from utils.ecc import Ecc
from tinyec import registry
import time

class MessageUsecase():
    message_repo: MessageRepository
    def __init__(self, db: Database) -> None:
        self.message_repo = MessageRepository(db)
    
    def noori_init(self):
        # Server select random curve
        ecc = Ecc(security_level=192)
        
        # then server select private key and calculate public key of card reader 
        start_time_rprk = time.time()
        reader_priv_key = ecc.generate_priv_key()
        time_rprk = time.time() - start_time_rprk

        start_time_rpuk = time.time()
        reader_pub_key = ecc.calculate_pub_key(reader_priv_key)
        time_rpuk = time.time() - start_time_rpuk

        # then server select private key and calculate public key of card
        start_time_cprk = time.time()
        card_priv_key = ecc.generate_priv_key()
        time_cprk = time.time() - start_time_cprk

        start_time_cpuk = time.time()
        card_pub_key = ecc.calculate_pub_key(card_priv_key)
        time_cpuk = time.time() - start_time_cpuk

        print()
        print("Reader Private Key Generation time : " + str(time_rprk) + " s")
        print("Reader Public Key Generation time : " + str(time_rpuk) + " s")
        print("Card Private Key Generation time : " + str(time_cprk) + " s")
        print("Card Public Key Generation time : " + str(time_cpuk) + " s")

    def encrypt_message(self, data: MessageRequest):
        # TODO : add function to encrypt mes
        # sage with ECC algorithm
        ecc = Ecc(security_level=192)
        reader_priv_key = ecc.generate_priv_key()
        reader_pub_key = ecc.calculate_pub_key(reader_priv_key)
        msg = bytes(data.msg, 'utf-8')
        encrypted_msg = ecc.encrypt(msg, reader_pub_key)
        print(encrypted_msg)
        field_g = list()
        for v in ecc.curve.field.g:
            field_g.append(str(v))
        data_to_be_stored = MessageEncryptedData(
            g_curve={
                'name': ecc.curve.name,
                'a': str(ecc.curve.a),
                'b': str(ecc.curve.b),
                'field': {
                    'p': str(ecc.curve.field.p),
                    'g': field_g,
                    'n': str(ecc.curve.field.n),
                    'h': str(ecc.curve.field.h)
                }
            },
            priv_key_reader=str(reader_priv_key),
            priv_key_tag=str(encrypted_msg[4]),
            plaintext=data.msg,
            nonce=encrypted_msg[1],
            tag=encrypted_msg[2]
        )
        self.message_repo.add_message(data_to_be_stored)
        res = {
            'ciphertext': encrypted_msg[0],
            'pub_key': ecc.get_pub_key_str(encrypted_msg[3]),
            'nonce': encrypted_msg[1]
        }
        return res

    def create_ecc(self, a, b, field, name):
        ecc = Ecc(security_level=192)
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
            
            field_g = list()
            for v in c['g_curve']['field']['g']:
                field_g.append(int(v))

            field = registry.ec.SubGroup(
                p=int(c['g_curve']['field']['p']),
                g=field_g,
                n=int(c['g_curve']['field']['n']),
                h=int(c['g_curve']['field']['h'])
            )
            ecc = self.create_ecc(a, b, field, name)
            pub_key_tag = ecc.calculate_pub_key(priv_key_tag)
            # pub_key_tag_str = str(pub_key_tag.x) + str(pub_key_tag.y) + str(pub_key_tag.p)
            pub_key_tag_hashed = ecc.get_pub_key_str(pub_key_tag)
            if (data.hashed_pub_key == pub_key_tag_hashed):
                msg = c
                break
        if (msg is not None):
            print("msg is not none")
            print(msg)
            #Decrypt Here
            priv_key_reader = int(c['priv_key_reader'])
            enctypted_msg = (
                data.ciphertext,
                data.nonce,
                msg['tag'],
                pub_key_tag,
                int(msg['priv_key_tag'])
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
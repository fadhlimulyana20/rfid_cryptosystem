from pymongo.database import Database
from repositories.message_repo import MessageRepository
from models.message import MessageRequest, MessageEncryptedData
from utils.ecc import Ecc

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
            plaintext=data.msg,
            ciphertext=encrypted_msg[0],
            g_curve=ecc.curve,
            priv_key_reader=reader_priv_key,
            pub_key_reader=reader_pub_key,
            priv_key_tag=encrypted_msg[4],
            pub_key_tag=encrypted_msg[4],
            algorithm="ecc"
        )
        print(ecc.curve)
        print()
        print(data_to_be_stored)
        result = self.message_repo.add_message(data_to_be_stored)
        return result

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
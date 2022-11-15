from usecase.message_usecase import MessageUsecase
from database.database import get_database
from models.message import MessageRequest, MessageDecryptData

def test_ecnrypt_message():
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

def test_decrypt_message():
    db = get_database()

    data = MessageRequest(
        msg="Test",
        algorithm="ecc",
        type="encrypt"
    )
    mu = MessageUsecase(db)
    res = mu.encrypt_message(data)

    data = MessageDecryptData(
        ciphertext=res['ciphertext'],
        hashed_pub_key=res['pub_key'],
        nonce=res['nonce']
    )
    r = mu.decrypt_message(data)
    print(r)
    assert True
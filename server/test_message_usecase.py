from usecase.message_usecase import MessageUsecase
from database.database import get_database
from models.message import MessageRequest   

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
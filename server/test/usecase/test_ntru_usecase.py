from usecase.ntru_usecase import NtruUsecase
from database.database import get_database

def test_ntru_generate():
    db = get_database()
    n = NtruUsecase(db)
    n.generate(1499, 2, 2039)
from pymongo.database import Database
from utils.ntru.ntrucipher import NtruCipher
import numpy as np
from models.keys import NTRUKeysReq
from repositories.keys_repo import KeysRepository

class NtruUsecase():
    keys_repo: KeysRepository
    def __init__(self, db: Database) -> None:
        self.keys_repo = KeysRepository(db=db)

    def generate(self, N, p, q):
        ntru = NtruCipher(N, p, q)
        ntru.generate_random_keys()
        h = np.array(ntru.h_poly.all_coeffs()[::-1])
        f, f_p = ntru.f_poly.all_coeffs()[::-1], ntru.f_p_poly.all_coeffs()[::-1]
        a = None
        np.savez_compressed("priv_key", N=N, p=p, q=q, f=f, f_p=f_p)
        np.savez_compressed("pub_key", N=N, p=p, q=q, h=h)
        # data = NTRUKeysReq(n=N, p=p, q=q, h=h_list, f=[1,2,3], f_p=[1,2,3])
        # self.keys_repo.add_ntru_key(data)
        # print("N: ", N)
        # print("p: ", p)
        # print("p: ", q)
        # print("h: ", h.tolist())
        # print("f: ", list(f))
        # print("fp: ", list(f_p))
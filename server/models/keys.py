from pydantic import BaseModel

class NTRUKeysReq(BaseModel):
    n: int
    p: int
    q: int
    h: list
    f: list
    f_p: list
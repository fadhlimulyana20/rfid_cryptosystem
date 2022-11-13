from pydantic import BaseModel

class MessageRequest(BaseModel):
    msg: str
    type: str
    algorithm: str

class MessageEncryptedResponse(BaseModel):
    ciphertext: str
    pub_key: str
    algorithm: str

class MessageDecryptedResponse(BaseModel):
    plaintext: str
    pub_key: str
    algorithm: str
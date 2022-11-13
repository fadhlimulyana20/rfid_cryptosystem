from pydantic import BaseModel

class MessageRequest(BaseModel):
    msg: str
    type: str
    algorithm: str

class MessageEncryptedData(BaseModel):
    plaintext: any
    ciphertext: any
    g_curve: any
    pub_key_tag: any
    priv_key_tag: any
    pub_key_reader: any
    priv_key_reader: any
    algorithm: any

class MessageEncryptedDataStored(BaseModel):
    id: any
    plaintext: any
    ciphertext: any
    g_curve: any
    pub_key_tag: any
    priv_key_tag: any
    pub_key_reader: any
    priv_key_reader: any
    algorithm: any

class MessageEncryptedResponse(BaseModel):
    ciphertext: str
    pub_key: str
    algorithm: str

class MessageDecryptedResponse(BaseModel):
    plaintext: str
    pub_key: str
    algorithm: str
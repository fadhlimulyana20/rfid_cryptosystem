from pydantic import BaseModel, validator
from typing import Union, Any
from tinyec import registry, ec

class MessageRequest(BaseModel):
    msg: str
    type: str
    algorithm: str

class MessageDecryptData(BaseModel):
    hashed_pub_key: str
    ciphertext: bytes
    nonce: bytes

class MessageEncryptedData(BaseModel):
    g_curve: Any
    priv_key_tag: str
    priv_key_reader: str
    plaintext: str
    nonce: bytes

# class MessageEncryptedData(BaseModel):
#     plaintext: str
#     ciphertext: bytes
#     g_curve: Any
#     pub_key_tag: Any
#     priv_key_tag: int
#     pub_key_reader: Any
#     priv_key_reader: int
#     algorithm: str

    # @validator('pub_key_tag')
    # def pub_key_tag_exists(cls, v):
    #     return v.pub_key_tag

    # @validator('pub_key_reader')
    # def pub_key_reader_exists(cls, v):
    #     return v.pub_key_reader

    class Config:
        arbitrary_types_allowed = True

class MessageEncryptedDataStored(BaseModel):
    id: str
    plaintext: str
    ciphertext: bytes
    g_curve: Any
    pub_key_tag: Any
    priv_key_tag: int
    pub_key_reader: Any
    priv_key_reader: int
    algorithm: str

    class Config:
        arbitrary_types_allowed = True

class MessageEncryptedResponse(BaseModel):
    ciphertext: str
    pub_key: str
    algorithm: str

class MessageDecryptedResponse(BaseModel):
    plaintext: str
    pub_key: str
    algorithm: str
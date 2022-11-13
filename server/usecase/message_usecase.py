from pymongo.database import Database
from repository.message_repo import MessageRepository
from models.message import MessageRequest

class MessageUsecase():
    message_repo: MessageRepository
    def __init__(self, db: Database) -> None:
        self.message_repo = MessageRepository(db)
    
    def encrypt_message(self, data:MessageRequest):
        # TODO : add function to encrypt message with ECC algorithm
        pass
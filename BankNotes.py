from pydantic import BaseModel

#1

class BankNote(BaseModel):
    variance :float
    skewness :float
    curtosis :float
    entropy :float
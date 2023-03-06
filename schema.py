from pydantic import BaseModel

class UserIn(BaseModel):
    name: str
    email: str
    quote: str

class UserOut(UserIn):
    id: int


class DiseaseIn(BaseModel):
    name: str
    symptom: str
    remedy: str

class DiseaseOut(DiseaseIn):

    name: str
    symptom: str
    remedy: str
    
    class Config:
        orm_mode = True
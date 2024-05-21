from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    __tablename__ = "users"
    login: str
    email: EmailStr
    password_hash: str


class UserCreate(UserBase):
    login: str
    password_hash: str


class UserLogin(UserBase):
    login: str
    password_hash: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



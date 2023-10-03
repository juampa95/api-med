import datetime
from enum import Enum
from typing import Optional
from pydantic import validator, EmailStr
from sqlmodel import SQLModel, Field, Relationship


class AccessLevel(str,Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    DOCTOR = 'DOCTOR'
    PATIENT = 'PATIENT'
    NURSE = 'NURSE'


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    username: str = Field(index=True)
    password: str = Field(max_length=256, min_length=6)
    email = EmailStr
    created_at: datetime.datetime = datetime.datetime.now()
    access_level: AccessLevel = Field(default=AccessLevel.USER)


class UserInput(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email = EmailStr
    access_level: AccessLevel = Field(default=AccessLevel.USER)

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords don\'t match')


class UserLogin(SQLModel):
    username: str
    password: str


class ChangePwd(SQLModel):
    newpassword: str = Field(max_length=256, min_length=6)
    newpassword2: str
    password: str

    @validator('newpassword2')
    def password_match(cls, v, values, **kwargs):
        if 'newpassword' in values and v != values['newpassword']:
            raise ValueError('passwords don\'t match')



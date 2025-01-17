import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Nullable
from typing_extensions import Optional


class BookBase(BaseModel):
    title: str = Field(description="Название книги")
    description: str = Field(description="Описание книги")
    publication_date: datetime = Field(description="Дата публикации")
    genre: str = Field(description="Жанр книги")
    available_copies: int = Field(description="Количество доступных экземпляров")


class AuthorBase(BaseModel):
    name: str = Field(description="Имя автора")
    biography: str = Field(description="Биография автора")
    birth_date: datetime = Field(description="Дата  рождения")

    # @field_validator("phone_number")
    # def validate_phone_number(cls, value: str) -> str:
    #     if not re.match(r'^\+\d{5,15}$', value):
    #         raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
    #     return value


class LBookAddDB(BookBase):
    author_id: int = Field(description="ID Автора книги")

class LBookUpdateDB(BaseModel):
    available_copies: int =Field(description="Кол-во доступных экземпляров")



class TransactionsBase(BaseModel):
    books_id: int = Field(description="Ссылка на книгу в таблице `books`")
    users_id: int = Field(description=" Ссылка на пользователя в таблице `users`")
    issue_date: datetime = Field(description="Дата выдачи книги")
    due_date: datetime = Field(description="Предполагаемая дата возврата")
    return_date: Optional[datetime] = None # Фактическая дата возврата(может быть null, если книга не возвращена)
    # return_date: datetime = None #Field(description="Фактическая дата возврата(может быть null, если книга не возвращена)",
                             #     default=None)

class LUserIReturn(BaseModel):
    users_id: int = Field(description="ID пользователя")
    return_date:  Optional[datetime] = None #(description="Фактическая дата возврата")
    # model_config = ConfigDict(from_attributes=True)

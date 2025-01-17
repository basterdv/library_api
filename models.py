from datetime import date

from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.dao.database import Base, str_uniq
from app.users.model import User


class Books(Base):
    __tablename__ = 'books'

    title: Mapped[str_uniq]  # Название книги
    description: Mapped[str]  # Описание книги
    publication_date: Mapped[date]  # Дата публикации
    genre: Mapped[str]  # Жанр книги
    available_copies: Mapped[int]  # Количество доступных экземпляров
    # - Автор(ы)(связь с таблицей авторов)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    authors: Mapped['Authors'] = relationship('Authors', back_populates='books')
    transactions: Mapped['Transactions'] = relationship('Transactions',back_populates='books')

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}"


class Authors(Base):
    __tablename__ = 'authors'

    name: Mapped[str_uniq]  # Имя автора
    biography: Mapped[str]  # Биография автора
    birth_date: Mapped[date]  # Дата рождения
    books: Mapped['Books'] = relationship('Books', back_populates='authors')
    # transactions: Mapped['Transactions'] = relationship('Transactions', back_populates='authors')

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}"


class Transactions(Base):
    __tablename__ = 'transactions'

    issue_date: Mapped[date] = mapped_column(Date)  # Дата выдачи книги.
    due_date: Mapped[date] = mapped_column(Date)  # Предполагаемая дата возврата.
    return_date: Mapped[date] = mapped_column(
        Date,nullable=True,server_default=None)  # Фактическая дата возврата(может быть null, если книга не возвращена)

    # Ссылка на книгу в таблице `books`.
    books_id: Mapped[int] = mapped_column(ForeignKey(
        'books.id', ondelete="CASCADE"), nullable=False)
    books:Mapped['Books'] = relationship('Books',back_populates='transactions')

    # Ссылка на пользователя в таблице `users`.
    users_id: Mapped[int] = mapped_column(ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    user:Mapped['User'] = relationship('User',back_populates='transactions')


    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}"

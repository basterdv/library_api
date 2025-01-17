from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.dao.database import Base, str_uniq


class User(Base):
    __tablename__ = 'user'

    phone_number: Mapped[str_uniq]  # Номер телефона
    first_name: Mapped[str]  # Имя
    last_name: Mapped[str]  # Фамилия
    email: Mapped[str_uniq]  # Электронная почта
    password: Mapped[str]  # Пароль
    # Роль администратора
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    transactions: Mapped['Transactions'] = relationship('Transactions', back_populates='user')

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

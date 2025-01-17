from app.dao.base import BaseDAO
from app.library_api.models import Authors,Books,Transactions


class BooksDAO(BaseDAO):
    model = Books

class AuthorDAO(BaseDAO):
    model = Authors

class TransactionsDAO(BaseDAO):
    model = Transactions


# class UsersDAO(BaseDAO):
#     model = Users
#
#     # @classmethod
#     # async def add_user(cls, session: AsyncSession, user_names: list[str]) -> list[int]:
#     #     """
#     #         Метод для добавления пользоватедей в базу данных.
#     #         Принимает список строк , проверяет, существуют ли в базе данных,
#     #         добавляет новые и возвращает список ID .
#     #
#     #         :param session: Сессия базы данных.
#     #         :param user_names: Список пользователей в нижнем регистре.
#     #         :return: Список ID .
#     #         """
#     #     user_id = []
#
#     @classmethod
#     async def get_users_list(cls, session: AsyncSession):
#         # Строим запрос
#         query = select(cls.model)
#
#         # Выполняем запрос
#         result = await session.execute(query)
#
#         # Извлекаем записи как объекты модели
#         users = result.scalars().all()
#
#         return users



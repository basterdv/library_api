from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import AuthorAlreadyExistsException, BookAlreadyExistsException, AuthorNotExistsException, \
    BookANotExistsException, BookOutOfStock, CountBookExceeded
from app.auth.dependencies import get_current_admin_user, get_current_user
from app.library_api.dao import AuthorDAO, BooksDAO, TransactionsDAO
from app.dao.session_maker import TransactionSessionDep
from app.library_api.schemas import BookBase, AuthorBase, LBookAddDB, TransactionsBase, LBookUpdateDB, LUserIReturn
from app.users.model import User
from app.admin.schemas import SUserID

router = APIRouter(prefix='/api', tags=['API_library'])


@router.post("/add_book/", summary="Добавить книгу.")
async def add_book(book_data: LBookAddDB, session: AsyncSession = TransactionSessionDep,
                   user_data: User = Depends(get_current_admin_user)) -> dict:
    book_data_dict = book_data.model_dump()

    author = await AuthorDAO.find_one_or_none(session, filters=SUserID(id=book_data.author_id))

    if author is None:
        raise AuthorNotExistsException

    try:
        await BooksDAO.add(session=session, values=LBookAddDB(**book_data_dict))
    except:
        raise BookAlreadyExistsException

    return {'message': f'Вы успешно добавили книгу!'}


@router.patch('/update_book_data/{book_id}', summary="Изменить данных книги")
async def update_book_data(book_data: BookBase, book_id: int, session: AsyncSession = TransactionSessionDep,
                           user_data: User = Depends(get_current_admin_user)):
    book_data_dict = book_data.model_dump()

    return await BooksDAO.update(session=session, filters=SUserID(id=book_id), values=BookBase(**book_data_dict))


@router.delete('/delete_book/{book_id}', summary="Удалить книгу.")
async def delete_book(book_id: int, session: AsyncSession = TransactionSessionDep,
                      user_data: User = Depends(get_current_admin_user)):
    return await BooksDAO.delete(session=session, filters=SUserID(id=book_id))


@router.post("/add_author/", summary="Добавить автора")
async def add_author(author_data: AuthorBase, session: AsyncSession = TransactionSessionDep,
                     user_data: User = Depends(get_current_admin_user)) -> dict:
    author_data_dict = author_data.model_dump()

    try:
        await AuthorDAO.add(session=session, values=AuthorBase(**author_data_dict), )
    except:
        raise AuthorAlreadyExistsException

    return {'message': f'Вы успешно добавили автора!'}


@router.patch('/update_author_data/{author_id}', summary="Изменить данные автора")
async def update_author_data(author_data: AuthorBase, author_id: int, session: AsyncSession = TransactionSessionDep,
                             user_data: User = Depends(get_current_admin_user)):
    author_data_dict = author_data.model_dump()

    return await AuthorDAO.update(session=session, filters=SUserID(id=author_id), values=AuthorBase(**author_data_dict))


@router.delete('/delete_author/{author_id}', summary="Удалить автора.")
async def delete_author(author_id: int, session: AsyncSession = TransactionSessionDep,
                        user_data: User = Depends(get_current_admin_user)):
    return await AuthorDAO.delete(session=session, filters=SUserID(id=author_id))


@router.post("/issuance_transactions/", summary="Транзакция на выдачу книги.")
async def issuance_transactions(transactions_data: TransactionsBase,
                                session: AsyncSession = TransactionSessionDep,
                                user_data: User = Depends(get_current_user)) -> dict:
    transactions_data_dict = transactions_data.model_dump()

    book = await BooksDAO.find_one_or_none_by_id(data_id=transactions_data.books_id, session=session)

    if book is None:
        raise BookANotExistsException

    # Проверяем наличие на складе
    count_book = book.available_copies  # Получаем кол-во экземпляров
    if count_book == 0:
        raise BookOutOfStock

    # Проверяем количество одновременно выдаваемых книг на одного читателя


    count_issuance_transactions = len(
        await TransactionsDAO.find_all(session=session, filters=LUserIReturn(users_id=user_data.id,return_date = None)))

    if count_issuance_transactions >= 5:
        raise CountBookExceeded

    # Подготавливаем данные
    transactions_data_dict['users_id'] = user_data.id  # Записываем ID авторизированного пользователя
    transactions_data_dict['return_date'] = None  # Дата возврата книги null

    book_data_dict = {'available_copies': count_book - 1}  # Изменяем кол-во экземпляров

    try:
        await BooksDAO.update(session=session, filters=SUserID(id=transactions_data.books_id),
                              values=LBookUpdateDB(**book_data_dict))

    except:
        raise BookANotExistsException

    await TransactionsDAO.add(session=session, values=TransactionsBase(**transactions_data_dict))

    return {'message': f'Вы успешно добавили транзакцию!'}


@router.post("/return_transactions/", summary="Транзакция на возврат книги.")
async def remove_transactions(transactions_data: TransactionsBase,
                              session: AsyncSession = TransactionSessionDep,
                              user_data: User = Depends(get_current_user)) -> dict:
    transactions_data_dict = transactions_data.model_dump()

    book = await BooksDAO.find_one_or_none_by_id(data_id=transactions_data.books_id, session=session)

    if book is None:
        raise BookANotExistsException

    count_book = book.available_copies  # Получаем кол-во экземпляров

    transactions_data_dict['users_id'] = user_data.id  # Записываем ID авторизированного пользователя
    book_data_dict = {'available_copies': count_book + 1}  # Изменяем кол-во экземпляров
    transactions_data_dict['return_date'] = '2025-01-14'

    # try:
    await BooksDAO.update(session=session, filters=SUserID(id=transactions_data.books_id),
                              values=LBookUpdateDB(**book_data_dict))

    await TransactionsDAO.add(session=session, values=TransactionsBase(**transactions_data_dict))

    # except:
    #     raise BookANotExistsException

    return {'message': f'Вы успешно добавили транзакцию!'}

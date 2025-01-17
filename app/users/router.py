from app.users.schemas import SUserAddDB, SUserRegister, SUserAuth
from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.dao import UsersDAO
from app.dao.session_maker import SessionDep, TransactionSessionDep
from app.users.schemas import EmailModel, SUserInfo, SUserUpdate
from app.admin.schemas import SUserID
from app.users.auth import authenticate_user, create_access_token
from exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException, ForbiddenException
from app.users.model import User
from app.auth.dependencies import get_current_user
from fastapi.responses import RedirectResponse

router = APIRouter(prefix='/api', tags=['API_users'])


@router.post("/register", summary="Регистрация пользователя.")
async def register_user(user_data: SUserRegister, session: AsyncSession = TransactionSessionDep) -> RedirectResponse:
    user = await UsersDAO.find_one_or_none(session, filters=EmailModel(email=user_data.email))

    if user:
        raise UserAlreadyExistsException

    user_data_dict = user_data.model_dump()
    del user_data_dict['confirm_password']

    try:
        await UsersDAO.add(session=session, values=SUserAddDB(**user_data_dict))
    except:
        raise UserAlreadyExistsException

    # return {'message': f'Вы успешно зарегистрированы!'}
    return RedirectResponse(url="/api/me")


@router.post("/login_user", summary="Авторизация пользователя.")
async def login_user(response: Response, user_data: SUserAuth, session: AsyncSession = SessionDep):
    check = await authenticate_user(session=session, email=user_data.email, password=user_data.password)

    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)

    return {'ok': True, 'access_token': access_token, 'message': 'Авторизация успешна!'}


@router.post("/logout/", summary="Выход пользователя.")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/me/", summary="Тест администратора.")
async def get_me(user_data: User = Depends(get_current_user)) -> SUserInfo:
    return SUserInfo.model_validate(user_data)


@router.patch('/change_user_data/{user_id}', summary="Изменить данные пользователя")
async def change_user_data(user_data: SUserUpdate, user_id: int, session: AsyncSession = TransactionSessionDep,
                           user: User = Depends(get_current_user), ):
    if user.id != user_id:
        raise ForbiddenException

    user_data_dict = user_data.model_dump()

    return await UsersDAO.update(session=session, filters=SUserID(id=user_id), values=SUserUpdate(**user_data_dict))

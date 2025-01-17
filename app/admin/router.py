from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.session_maker import SessionDep, TransactionSessionDep
from app.users.model import User
from app.auth.dependencies import get_current_admin_user
from typing import List
from app.users.schemas import SUserInfo
from app.users.dao import UsersDAO
from app.admin.schemas import SUserID, SUserRole


router = APIRouter(prefix='/api', tags=['API_admin'])


@router.get("/all_users/",summary="Просмотр всех пользователей.")
async def get_all_users(session: AsyncSession = SessionDep,
                        user_data: User = Depends(get_current_admin_user)) -> List[SUserInfo]:
    return await UsersDAO.find_all(session=session, filters=None)


@router.delete('/delete_user/{user_id}', summary="Удалить пользователя")
async def delete_user(user_id: int, session: AsyncSession = TransactionSessionDep,
                      user_data: User = Depends(get_current_admin_user)):
    return await UsersDAO.delete(session=session, filters=SUserID(id=user_id))


@router.patch('/change_status/{user_id}', summary="Изменить статус пользователя")
async def change_admin_status(user_id: int, new_status: bool, session: AsyncSession = TransactionSessionDep,
                              user_data: User = Depends(get_current_admin_user)):
    # return await UsersDAO.find_one_or_none_by_id(session=session,data_id=user_id)
    return await UsersDAO.update(session=session, filters=SUserID(id=user_id),
                                 values=SUserRole(is_admin=new_status))


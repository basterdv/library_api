from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.session_maker import SessionDep
from starlette.templating import _TemplateResponse
from app.library_api.dao import BooksDAO
from app.auth.dependencies import get_current_user

router = APIRouter(tags=['Фронтэнд'])

templates = Jinja2Templates(directory='app/templates')

@router.get("/")
def home_page(request: Request):
    context = {
        "request": request,
        # "posts": posts,
        "title": "Home Page",
        "isIndex": True
    }

    response = templates.TemplateResponse("/index.html", context)
    return response

@router.get("/login", summary="Авторизация пользователя.")
async def login_page(request: Request) :

    context = {
        "request": request,
        # "posts": posts,
        "title": "Login Page",
        "isLogin": True
    }

    response = templates.TemplateResponse("/login.html", context)
    return response


@router.get("/catalog", summary="Каталог книг.")
async def catalog_page(request: Request, session: AsyncSession = SessionDep) -> _TemplateResponse:
    list_books = []
    data = await BooksDAO.find_all(session=session, filters=None)
    for i in data:
        book = {'title': i.title, 'genre': i.genre, 'description': i.description,
                'publication_date': i.publication_date}
        list_books.append(book)

    context = {
        "request": request,
        "data": list_books,
        "title": "Catalog Page",
        "isCatalog":True
    }

    response = templates.TemplateResponse("/catalog.html", context)
    return response

@router.get("/profile", summary="Каталог книг.")
async def profile_page(request: Request,profile=Depends(get_current_user)) :


    context = {
        "request": request,
        "title": "Profile Page",
        'profile': profile,
        "isProfile":True
    }

    response = templates.TemplateResponse("/profile.html", context)
    return response



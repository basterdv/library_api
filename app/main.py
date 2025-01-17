from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.users.router import router as router_user
from app.admin.router import router as router_admin
from app.library_api.router import router as router_library_api
from app.pages.router import router as router_pages

import pathlib
from fastapi.templating import Jinja2Templates


app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=[
    BASE_DIR / "templates",
])

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router_user)
app.include_router(router_admin)
app.include_router(router_library_api)
app.include_router(router_pages)



# @app.get("/")
# async def redirect_to_auth():
#     return RedirectResponse(url="/api/login")

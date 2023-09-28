from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST, HTTP_303_SEE_OTHER
from starlette_admin.exceptions import FormValidationError, LoginFailed

from src.middlewares import login_user
from src.routers.templates import templates

router = APIRouter()


@router.get("/index")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()


@router.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "_is_login_path": True},
    )


@router.post("/login")
async def login(request: Request):
    form = await request.form()
    try:
        return await login_user(
            form.get("username"),  # type: ignore
            form.get("password"),  # type: ignore
            request,
            RedirectResponse(
                request.query_params.get("next")
                or request.url_for("index"),
                status_code=HTTP_303_SEE_OTHER,
            ),
        )
    except FormValidationError as errors:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "form_errors": errors, "_is_login_path": True},
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except LoginFailed as error:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": error.msg, "_is_login_path": True},
            status_code=HTTP_400_BAD_REQUEST,
        )

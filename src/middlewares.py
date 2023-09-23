from urllib.parse import urlencode

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.status import HTTP_303_SEE_OTHER
from starlette.types import ASGIApp
from starlette_admin.exceptions import FormValidationError, LoginFailed

users = {
    "admin": {
        "name": "Admin",
        "roles": ["admin"],
        "password": "admin"
    }
}


async def login_user(
        username: str,
        password: str,
        request: Request,
        response: Response,
) -> Response:
    if len(username) < 3:
        """Form data validation"""
        raise FormValidationError(
            {"username": "Ensure username has at least 03 characters"}
        )

    if username in users and password == users[username]['password']:
        """Save `username` in session"""
        request.session.update({"username": username})
        return response

    raise LoginFailed("Invalid username or password")


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        super().__init__(app)

        self.allow_paths = [
                "/login",
                "/statics/css/tabler.min.css",
                "/statics/css/fontawesome.min.css",
                "/statics/js/vendor/jquery.min.js",
                "/statics/js/vendor/tabler.min.js",
                "/statics/js/vendor/js.cookie.min.js",
            ]

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) in users:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            request.state.user = users.get(request.session["username"])
            return True

        return False

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if await self.is_authenticated(request) or request.scope['path'] in self.allow_paths:
            return await call_next(request)

        return RedirectResponse(
            "{url}?{query_params}".format(
                url="/login",
                query_params=urlencode({"next": str(request.url)}),
            ),
            status_code=HTTP_303_SEE_OTHER,
        )

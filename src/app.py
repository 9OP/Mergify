from fastapi import APIRouter, Depends, FastAPI, Request
from dotenv import load_dotenv
from os import path, environ
from fastapi.logger import logger
from logging import getLogger

from .clients.github import GithubClient
from .models.starneighbours import Starneighbours
from .services.starneighbours import Service as StarneighboursService
from .responses import setup_exception_handlers, AuthError


router = APIRouter()


def starneighbours_service():
    client = GithubClient(token=environ.get("GITHUB_TOKEN", ""))
    service = StarneighboursService(client=client)
    return service


async def require_authentication(req: Request):
    headers = req.headers
    authorization = headers.get("Authorization")

    if not authorization:
        raise AuthError()

    # Format should be: `Authorization: Bearer <token>`
    bearer = authorization.split(" ")[-1]
    if not bearer:
        raise AuthError()

    stagazer_token = environ.get("STARGAZER_TOKEN")
    if bearer != stagazer_token:
        raise AuthError()


async def endpoint(
    owner: str,
    repo: str,
    user_limit: int = 10,
    service: StarneighboursService = Depends(starneighbours_service),
):
    starneighbours = await service.get_starneighbours(
        owner=owner,
        repo=repo,
        user_limit=user_limit,
    )
    return starneighbours


router.add_api_route(
    path="/repos/{owner:str}/{repo:str}/starneighbours",
    methods=["GET"],
    endpoint=endpoint,
    response_model=list[Starneighbours],
    dependencies=[Depends(require_authentication)],
    description="Return the list of starneighbours for given repo",
)


def load_config():
    dotenv_file = path.join(path.dirname(__file__), "../.env")
    if path.exists(dotenv_file):
        load_dotenv(dotenv_file)


def set_logger():
    uvicorn_logger = getLogger("uvicorn")
    logger.handlers = uvicorn_logger.handlers
    logger.setLevel(uvicorn_logger.level)


def create_app() -> FastAPI:
    load_config()
    set_logger()

    app = FastAPI()
    app.include_router(router)
    setup_exception_handlers(app)

    return app

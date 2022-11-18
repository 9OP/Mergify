from fastapi import APIRouter, Depends, FastAPI


from .clients.github import GithubClient
from .models.starneighbours import Starneighbours
from .services.starneighbours import Service as StarneighboursService
from .responses import setup_exception_handlers


router = APIRouter()


def starneighbours_service():
    client = GithubClient()
    service = StarneighboursService(client=client)
    return service


async def endpoint(
    owner: str,
    repo: str,
    user_limit: int = 20,
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
    description="Return the list of starneighbours for given repo",
)


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    setup_exception_handlers(app)

    return app

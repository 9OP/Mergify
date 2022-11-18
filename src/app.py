from fastapi import APIRouter, Depends, FastAPI


from .github_client import GithubClient
from .starneighbours import Service as StarneighboursService


router = APIRouter()


def starneighbours_service():
    repository = GithubClient()
    service = StarneighboursService(repository=repository)
    return service


async def endpoint(
    user: str,
    repo: str,
    service: StarneighboursService = Depends(starneighbours_service),
):
    starneighbours = await service.get_starneighbours(user=user, repo=repo)
    return starneighbours


router.add_api_route(
    path="/repos/{user:str}/{repo:str}/starneighbours",
    methods=["GET"],
    endpoint=endpoint,
)


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app

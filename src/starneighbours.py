from abc import ABC, abstractmethod
from collections import defaultdict


from .models import Stargazer, GithubRepo, Starneighbours


class Repository(ABC):
    @abstractmethod
    async def get_stargazers(
        self, owner: str, repo: str, count: int
    ) -> list[Stargazer]:
        pass

    @abstractmethod
    async def get_starred(self, user: str, count: int) -> list[GithubRepo]:
        pass


class Service:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    async def get_starneighbours(self, user: str, repo: str) -> list[Starneighbours]:
        # Store stargazers name list for repo name
        starneighbours_dict: dict[str, list[str]] = defaultdict(list)
        stargazers = await self._repository.get_stargazers(
            owner=user,
            repo=repo,
            count=2,
        )
        for stargazer in stargazers:
            for gh_repo in await self._repository.get_starred(stargazer.name, count=4):
                starneighbours_dict[gh_repo.name].append(stargazer.name)

        starneighbours: list[Starneighbours] = []
        for repo_name, stargazers_list in starneighbours_dict.items():
            starneighbours.append(
                Starneighbours(
                    repo=repo_name,
                    stargazers=stargazers_list,
                )
            )

        return starneighbours

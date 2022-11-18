from abc import ABC, abstractmethod
from collections import defaultdict
from asyncio import create_task, gather, Task
from functools import partial


from src.models.starneighbours import Stargazer, GithubRepo, Starneighbours


class Client(ABC):
    @abstractmethod
    async def get_stargazers(
        self, owner: str, repo: str, count: int
    ) -> list[Stargazer]:
        pass

    @abstractmethod
    async def get_starred(self, user: str, count: int) -> list[GithubRepo]:
        pass


StarneighboursDict = dict[str, list[str]]


class Service:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def get_starneighbours(
        self, owner: str, repo: str, user_limit: int
    ) -> list[Starneighbours]:
        stargazers = await self._client.get_stargazers(
            owner=owner,
            repo=repo,
            count=user_limit,
        )
        starneighbours = await self.__fetch_starneighbours_in_parallel(stargazers)
        return self.__format_starneighbours(starneighbours)

    async def __fetch_starneighbours_in_parallel(
        self, stargazers: list[Stargazer]
    ) -> StarneighboursDict:
        starneighbours_dict: StarneighboursDict = defaultdict(list)

        async def fetch_starneighbours(stargazer_name: str):
            gh_repos = await self._client.get_starred(stargazer_name, count=4)
            for gh_repo in gh_repos:
                starneighbours_dict[gh_repo.name].append(stargazer_name)

        tasks: list[Task] = []
        for stargazer in stargazers:
            pfunc = partial(fetch_starneighbours, stargazer.name)
            task = create_task(pfunc())
            tasks.append(task)

        await gather(*tasks, return_exceptions=True)

        return starneighbours_dict

    @staticmethod
    def __format_starneighbours(
        starneighbours_dict: StarneighboursDict,
    ) -> list[Starneighbours]:
        starneighbours: list[Starneighbours] = []

        for repo_name, stargazers_list in starneighbours_dict.items():
            neighbour = Starneighbours(
                repo=repo_name,
                stargazers=stargazers_list,
            )
            starneighbours.append(neighbour)

        return starneighbours

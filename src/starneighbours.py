from abc import ABC, abstractmethod
from collections import defaultdict
from asyncio import Queue, create_task, gather, Task


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


StarneighboursDict = dict[str, list[str]]


class Service:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    async def get_starneighbours(self, user: str, repo: str) -> list[Starneighbours]:
        stargazers = await self._repository.get_stargazers(
            owner=user,
            repo=repo,
            count=2,
        )

        starneighbours = await self.__fetch_starneighbours_in_parallel(stargazers)

        return self.__format_starneighbours(starneighbours)

    async def __fetch_starneighbours_in_parallel(
        self, stargazers: list[Stargazer]
    ) -> StarneighboursDict:
        starneighbours_dict: StarneighboursDict = defaultdict(list)
        queue: Queue[str] = Queue()
        tasks: list[Task] = []
        tasks_num = 5

        for stargazer in stargazers:
            queue.put_nowait(stargazer.name)

        for _ in range(tasks_num):
            task = create_task(self.__fetch_starred(queue, starneighbours_dict))
            tasks.append(task)

        await queue.join()

        for task in tasks:
            task.cancel()

        await gather(*tasks, return_exceptions=True)

        return starneighbours_dict

    async def __fetch_starred(
        self, queue: Queue[str], starneighbours_dict: StarneighboursDict
    ):
        while True:
            stargazer_name = await queue.get()

            gh_repos = self._repository.get_starred(stargazer_name, count=4)
            for gh_repo in await gh_repos:
                starneighbours_dict[gh_repo.name].append(stargazer_name)

            queue.task_done()

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

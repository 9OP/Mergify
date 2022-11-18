import aiohttp
from contextlib import asynccontextmanager

from .starneighbours import Repository
from .models import Stargazer, GithubRepo


@asynccontextmanager
async def aio_session():
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()


class GithubClient(Repository):
    async def get_stargazers(
        self, owner: str, repo: str, count: int
    ) -> list[Stargazer]:
        # DOCS: https://docs.github.com/en/rest/activity/starring
        #       per_page max is 100
        async with aio_session() as session:
            res = await session.get(
                url=f"https://api.github.com/repos/{owner}/{repo}/stargazers",
                headers={"Accept": "application/vnd.github+json"},
                params={"per_page": count},
            )
        data = await res.json()
        print(data)

        # TODO: handle error case when data does not contains stargazers
        stargazers: list[Stargazer] = []
        for stargazer in data:
            stargazers.append(Stargazer(name=stargazer["login"]))

        return stargazers

    async def get_starred(self, user: str, count: int) -> list[GithubRepo]:
        # DOCS: https://docs.github.com/en/rest/activity/starring
        #       per_page max is 100
        async with aio_session() as session:
            res = await session.get(
                url=f"https://api.github.com/users/{user}/starred",
                headers={"Accept": "application/vnd.github+json"},
                params={"per_page": count},
            )
        data = await res.json()

        # TODO: handle error case when data does not contains repositories
        gh_repositories: list[GithubRepo] = []
        for repo in data:
            gh_repositories.append(GithubRepo(name=repo["name"]))

        return gh_repositories

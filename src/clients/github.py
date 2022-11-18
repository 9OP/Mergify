import aiohttp
from contextlib import asynccontextmanager

from src.responses import GithubError
from src.services.starneighbours import Client
from src.models.starneighbours import Stargazer, GithubRepo


@asynccontextmanager
async def aio_session():
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()


class GithubClient(Client):
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

            if not res.ok:
                raise GithubError(res.status, str(res.reason))

        data = await res.json()

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

            if not res.ok:
                raise GithubError(res.status, str(res.reason))

        data = await res.json()

        gh_repositories: list[GithubRepo] = []
        for repo in data:
            gh_repositories.append(GithubRepo(name=repo["name"]))

        return gh_repositories

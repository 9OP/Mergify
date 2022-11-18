from aiohttp import ClientSession
from contextlib import asynccontextmanager
from os import environ


from src.responses import GithubError
from src.services.starneighbours import Client
from src.models.starneighbours import Stargazer, GithubRepo


@asynccontextmanager
async def aio_session():
    session = ClientSession()
    try:
        yield session
    finally:
        await session.close()


class GithubClient(Client):
    def __init__(self, token: str):
        self.token = token

    def headers(self) -> dict:
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {environ.get('GITHUB_TOKEN')}"
        return headers

    async def get_stargazers(
        self, owner: str, repo: str, count: int
    ) -> list[Stargazer]:
        # DOCS: https://docs.github.com/en/rest/activity/starring
        #       per_page max is 100
        page = 1
        data = []

        async with aio_session() as session:
            while count > 0:
                res = await session.get(
                    url=f"https://api.github.com/repos/{owner}/{repo}/stargazers",
                    headers=self.headers(),
                    params={"per_page": count, "page": page},
                )

                count = max(0, count - 100)

                if not res.ok:
                    raise GithubError(res.status, str(res.reason))

                page += 1
                data += await res.json()

        stargazers: list[Stargazer] = []
        for stargazer in data:
            stargazers.append(Stargazer(name=stargazer["login"]))

        return stargazers

    async def get_starred(self, user: str) -> list[GithubRepo]:
        # DOCS: https://docs.github.com/en/rest/activity/starring
        #       per_page max is 100
        page = 1
        data = []

        async with aio_session() as session:
            # It's too expensive to fetch all starred repo of a user.
            # Some user sadly have hundreds of repo
            # while True:
            res = await session.get(
                url=f"https://api.github.com/users/{user}/starred",
                headers=self.headers(),
                params={"per_page": 100, "page": page},
            )
            if not res.ok:
                raise GithubError(res.status, str(res.reason))

            page += 1
            json = await res.json()
            data += json
            # if len(json) == 100:
            #     continue
            # break

        gh_repositories: list[GithubRepo] = []
        for repo in data:
            gh_repositories.append(GithubRepo(name=repo["name"]))

        return gh_repositories

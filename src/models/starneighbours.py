from pydantic import BaseModel


class Stargazer(BaseModel):
    name: str


class GithubRepo(BaseModel):
    name: str


class Starneighbours(BaseModel):
    repo: str
    stargazers: list[str]

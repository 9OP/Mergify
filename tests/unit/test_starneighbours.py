import unittest

from src.services.starneighbours import Service, Client
from src.models.starneighbours import Stargazer, GithubRepo


class MockClient(Client):
    async def get_stargazers(
        self, owner: str, repo: str, count: int
    ) -> list[Stargazer]:
        return []

    async def get_starred(self, user: str) -> list[GithubRepo]:
        return []


class TestStarneighboursService(unittest.TestCase):
    def setUp(self):
        service = Service(MockClient())
        self.service = service

    def test_upper(self):
        pass


if __name__ == "__main__":
    unittest.main()

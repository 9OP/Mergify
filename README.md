# [Stargazers](https://mergify.notion.site/Stargazer-4cf5427e34a542f0aee4e829bb6d9035)

```sh
# Dependencies
poetry config virtualenvs.in-project true       # set .venv in local directory
source $(poetry env info --path)/bin/activate   # activate env
poetry install                                  # install dependencies

# Pre-commit hooks
pre-commit install
pre-commit run --all-files

# Run server
./run.sh
```

Or via Docker

```sh
# Build image
docker build -t stargazer .

# Start container
docker run -v $(pwd):/app -p 8080:8080 stargazer
```



TODO:
- ok implements endpoint
- ok - add uvicorn
- ok - add pre commit hook (black, flake8)
- add logging
- ok update architecture (domain, usecase, infrastructure)
- ok add docker
- add tests
- add authentication (via session cookie + .env credentials)

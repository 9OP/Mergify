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

# Send request to server
curl http...
```



TODO:
- implements endpoint
- ok - add uvicorn
- ok - add pre commit hook (black, flake8)
- add logging
- update architecture (domain, usecase, infrastructure)
- add docker
- add tests
- add authentication (via session cookie + .env credentials)

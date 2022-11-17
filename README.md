# Stargazers

```
poetry config virtualenvs.in-project true       # set .venv in local directory
source $(poetry env info --path)/bin/activate   # activate env
poetry install                                  # install dependencies
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

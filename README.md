# [Stargazers](https://mergify.notion.site/Stargazer-4cf5427e34a542f0aee4e829bb6d9035)

## Install and run
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

...Or via Docker
```sh
# Build image
docker build -t stargazer .

# Start container
docker run -v $(pwd):/app -p 8080:8080 stargazer
```

Test endpoint
```sh
curl --header "Authorization: Bearer stargazer_secret" http://localhost:8080/repos/apple/swift/starneighbours\?user_limit\=3
```

## Config
Config is simple and defined in `.env`:
```ini
GITHUB_TOKEN    = <token>
STARGAZER_TOKEN = <secret>
```

## Automated tests
Unit and functionnal tests are available in `./tests` with stdlib unittest (though I like pytest better).
```sh
python3 -m unittest discover -s tests -v
```

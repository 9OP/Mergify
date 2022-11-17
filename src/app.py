import fastapi


router = fastapi.APIRouter()


async def root():
    return {"message": "Hello World"}


router.add_api_route(
    path="/",
    methods=["GET"],
    endpoint=root,
)


def create_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    app.include_router(router)

    return app

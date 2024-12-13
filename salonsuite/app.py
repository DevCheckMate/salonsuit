
from fastapi import FastAPI
from salonsuite.routers import v1_routers



def create_app() -> FastAPI:
    ...
    app = FastAPI(
        title='Salon Suite', 
        version='0.1.0', 
        description='Saas Salão'
    )
    app.include_router(v1_routers)

    return app


app = create_app()
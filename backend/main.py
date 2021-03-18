from fastapi import FastAPI
from starlette.responses import RedirectResponse

from config.database import Base, engine
from api import router


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)


@app.get('/')
def root():
    return RedirectResponse(url='/docs/')

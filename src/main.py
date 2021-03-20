from fastapi import FastAPI
from starlette.responses import RedirectResponse

from api import router


app = FastAPI(title='SimpleToDoList', version='0.0.1')
app.include_router(router)


@app.get('/')
def root():
    return RedirectResponse(url='/docs/')

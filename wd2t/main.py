from fastapi import FastAPI

from wd2t.routes import decisions, tags

app = FastAPI()

app.include_router(decisions.router)
app.include_router(tags.router)

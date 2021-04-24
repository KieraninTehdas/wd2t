from fastapi import FastAPI

from wd2t.config import Config
from wd2t.routes import decisions, tags

app = FastAPI()

config = Config()

app.include_router(decisions.router, prefix=config.root_url_prefix)
app.include_router(tags.router, prefix=config.root_url_prefix)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from wd2t.config import Config
from wd2t.routes import decisions, tags

app = FastAPI()

config = Config()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(decisions.router, prefix=config.root_url_prefix)
app.include_router(tags.router, prefix=config.root_url_prefix)

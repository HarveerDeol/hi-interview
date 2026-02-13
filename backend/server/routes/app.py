from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.business.auth.auth_verifier import AuthVerifier
from server.routes.routes import get_all_routes
from server.shared.config import Config, Env
from server.shared.databasemanager import DatabaseManager

load_dotenv()

config = Config.from_env()
database = DatabaseManager.from_url(config.database_url)
auth_verifier = AuthVerifier(config)

app = FastAPI(
    title="Hi Interview",
    docs_url=None if config.env == Env.PROD else "/docs",
    redoc_url=None if config.env == Env.PROD else "/redoc",
    openapi_url=None if config.env == Env.PROD else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_all_routes(config, database, auth_verifier))

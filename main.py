from fastapi import FastAPI
from src.api.main_router import main_router
from src.database.db import make_databases_connection, disconnect_databases

app = FastAPI()
main_router(app=app)

app.add_event_handler("startup",make_databases_connection)
app.add_event_handler("shutdown",disconnect_databases)

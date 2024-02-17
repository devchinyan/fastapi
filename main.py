from fastapi import FastAPI
from src.api.main_router import main_router
from src.database.db import make_databases_connection, disconnect_databases

# Create an instance of the FastAPI class
app = FastAPI()
main_router(app=app)

app.add_event_handler("startup",make_databases_connection)
app.add_event_handler("shutdown",disconnect_databases)

# @app.on_event("startup")
# async def startup():
#     await make_databases_connection(app)

# @app.on_event("shutdown")
# async def shutdown():
#     await disconnect_databases(app)
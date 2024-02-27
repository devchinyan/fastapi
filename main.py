from fastapi import FastAPI, Request
from src.api.main_router import main_router
from src.database.db import make_databases_connection, disconnect_databases
from src.config.config import config
import json

# Create an instance of the FastAPI class
app = FastAPI()
main_router(app=app)

# @app.get("/r")
# async def request_handler(req:Request):
#     param = req.query_params
#     headers  = req.headers
#     return {"status":200, "param":param, 'keys':list(param.keys()), "method":req.method, "headers":headers}

# @app.post("/echo")
# async def post_request_handler(req:Request):
#     try:
#         body = await req.body()
#         body = body.decode()
#         body = json.loads(body)
        
#         keys = list(body.keys())

#         m = req.method

#         return {"status":200, "param":body, "type": type(body).__name__, "keys":keys , "method":m}
#     except Exception as err:
#         return {"status":500, "err":str(err)}

print(config)
app.add_event_handler("startup",make_databases_connection)
app.add_event_handler("shutdown",disconnect_databases)

# @app.on_event("startup")
# async def startup():
#     await make_databases_connection(app)

# @app.on_event("shutdown")
# async def shutdown():
#     await disconnect_databases(app)
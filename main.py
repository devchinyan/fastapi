from fastapi import FastAPI
from src.api.v1.public.public_router import public_router

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route for the root URL
app.include_router(public_router,prefix="")



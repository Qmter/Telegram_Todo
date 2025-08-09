from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import database
from api.endpoints import todo, users

@asynccontextmanager
async def lifespan(app: FastAPI):

    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

# app.include_router(users.router)
app.include_router(todo.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)

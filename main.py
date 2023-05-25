from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions import StoryException
from router import blog_get, user, article
from router import blog_post
from db import models
from db.database import engine

app = FastAPI()
app.include_router(user.router)
app.include_router(article.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

@app.get('/')
def index():
    return 'Hello World!!'

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )

models.Base.metadata.create_all(engine)
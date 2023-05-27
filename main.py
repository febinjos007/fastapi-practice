from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from auth import authentication
from exceptions import StoryException
from router import blog_get, user, article, product, blog_post, file
from db import models
from db.database import engine

app = FastAPI()
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(file.router)
app.include_router(article.router)
app.include_router(product.router)
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

# Below set of code helps in handling CORS error when trying to connect to a local app.
# You can define n number of origins in the below list and pas it to the middleware
origins = [
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.mount('/files', StaticFiles(directory="files"), name="files")
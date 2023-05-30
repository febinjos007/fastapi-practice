from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from auth import authentication
from exceptions import StoryException
from router import blog_get, user, article, product, blog_post, file
from db import models
from db.database import engine
from templates import templates
import time

app = FastAPI()
app.include_router(authentication.router)
app.include_router(templates.router)
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

# Adding a middleware to the service.
# Middle helps in intercepting the request and response and doing some logic in between.
# Following middleware will check the time taken for calls
@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return duration

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
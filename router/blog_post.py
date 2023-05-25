from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

class Image(BaseModel):
    url: str
    alias: str
class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]
    tags: Optional[List[str]] = []
    metadata: Dict[str, str] = {"key1": "val1"}
    image: Optional[Image] = None

@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        'id': id,
        'data': blog,
        'version': version
    }

@router.post('/new/{id}/comment/{comment_id}')
def create_comment(blog: BlogModel, id: int,
                   comment_id: int = Path(gt=5, le=10),
                   comment_title: int = Query(None,
                                           title="Id of the comment",
                                           description="Some description for comment_title",
                                           alias="commentTitle",
                                           deprecated=True),
                   content: str = Body("hi how are you"),
                   author: str = Body(...,
                                      min_length=10,
                                      regex='^[a-z\s]*$'),
                   v: Optional[List[str]] = Query(None)):
    return {
        'id': id,
        'data': blog,
        'comment_title': comment_title,
        'comment_id': comment_id,
        'content': content,
        'author': author,
        'version': v
    }

def required_functionality():
    return {'messsage': 'Learning FastApi is important'}
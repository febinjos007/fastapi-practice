from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
import shutil

router = APIRouter(
    prefix='/file',
    tags=['file']
)

# Note the following get end point uses bytes for handling file.
# This will have a size constraint to it. You won't be able to process large file using this approach
@router.post('/file')
def get_file(file: bytes = File(...)):
    content = file.decode('utf-8')
    lines = content.split('\n')
    return {
        'lines': lines
    }

# UploadFile module helps in processing bigger files and images
@router.post('/uploadfile')
def get_uploadfile(upload_file: UploadFile = File(...)):
    path = f'files/{upload_file.filename}'
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return {
        'filename': path,
        'type': upload_file.content_type
    }

@router.get('/download/{name}', response_class=FileResponse)
def get_file(name: str):
    path = f'/files/{name}'
    return path
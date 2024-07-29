
from fastapi import FastAPI, File, UploadFile,requests
from dotenv import load_dotenv
from fastapi import APIRouter,HTTPException
from starlette.responses import FileResponse
from utils import logger
from fastapi.responses import JSONResponse
import shutil
import os

# Load variables from .env file
load_dotenv()

# setting router
attachment_router = APIRouter()

# getting file server path from env file
file_server_path = os.getenv('file_server_path')



# query function for searching the files based on file name
@attachment_router.get("/{unique_filename}/")
async def get_file(unique_filename: str):
    file_path = os.path.join(file_server_path, unique_filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        return {"message": "File not found"}

    # Serve the file using FastAPI's FileResponse
    return FileResponse(file_path)



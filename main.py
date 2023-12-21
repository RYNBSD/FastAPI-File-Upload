from typing import LiteralString
from fastapi import FastAPI, status, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from os import getcwd
from os.path import join

ROOT_DIR: LiteralString = getcwd()
PUBLIC_DIR: LiteralString = join(ROOT_DIR, "public")

app = FastAPI()

def writeFile(path: str, content: bytes) -> None:
    with open(path, "wb") as file:
        file.write(content)
        file.close()

@app.post("/file", status_code=status.HTTP_200_OK, tags=["upload"])
async def uploadFile(file: UploadFile = File()):
    filePath = join(PUBLIC_DIR, file.filename)
    fileContent = await file.read()
    writeFile(filePath, fileContent)
    file.file.close()

    return JSONResponse({
        "success": True
    }, status.HTTP_200_OK)

@app.post("/files", status_code=status.HTTP_200_OK, tags=["upload"])
async def uploadFiles(files: list[UploadFile] = File()):
    for file in files:
        filePath = join(PUBLIC_DIR, file.filename)
        fileContent = await file.read()
        writeFile(filePath, fileContent)
        file.file.close()
    
    return JSONResponse({
        "success": True
    }, status.HTTP_200_OK)

app.mount("/", StaticFiles(directory=PUBLIC_DIR), name="public")
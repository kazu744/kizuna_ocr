from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path

app = FastAPI()

UPLOAD_DIR = Path(r"C:\OCR\uploads")

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.post('/upload')
async def upload(file: UploadFile = File(...)):
    contents = await file.read()

    return {"filename": file.filename, "size": len(contents)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.ocr.vision import detect_text_from_image
from app.chatgpt.chatgpt import extract_structure_data_from_text

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get('/upload', response_class=HTMLResponse)
def get_upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post('/upload')
async def upload(request: Request, file: UploadFile = File(...)):
    contents = await file.read()

    ocr_text = detect_text_from_image(contents)
    structured_data = extract_structure_data_from_text(ocr_text)

    print(f"アップロードファイル: {file.filename}")
    print(f"OCR結果:\n{structured_data}")

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "structured_data": structured_data
    })
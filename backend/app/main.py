from fastapi import FastAPI, File, UploadFile, Request
from typing import Optional
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.model.Ocr import Ocr

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
async def upload(request: Request, new_owner_inkan: Optional[UploadFile] = File(None)):
    if new_owner_inkan:
        contents = await new_owner_inkan.read()
        ocr_text = detect_text_from_image(contents)
        structured_data = extract_structure_data_from_text(ocr_text, document_type="new_owner_inkan")

        print(f"アップロードファイル: {new_owner_inkan.filename}")
        print(f"OCR結果:\n{structured_data}")

        ocr_record = Ocr.create(
            user_id=1,
            new_owner_name=structured_data.get("new_owner_name"),
            new_owner_address_main=structured_data.get("new_owner_address_main"),
            new_owner_address_street=structured_data.get("new_owner_address_street"),
            new_owner_address_number=structured_data.get("new_owner_address_number"),
            raw_text=ocr_text,
            created_at=datetime.now()
        )

        if ocr_record:
            return RedirectResponse(url="/upload", status_code=303)

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "structured_data": structured_data
    })
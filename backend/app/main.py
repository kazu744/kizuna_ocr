from fastapi import FastAPI, File, UploadFile, Request, Form, Response
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

@app.get('/list/{user_id}')
def show_list(request: Request, user_id: int):
    ocrs = Ocr.get_by_user(user_id=user_id)
    return templates.TemplateResponse("list.html", {
        "request": request,
        "ocrs": ocrs
        })
    
@app.get("/edit/{ocr_id}", response_class=HTMLResponse)
def get_edit_list(request: Request, ocr_id: int):
    ocr = Ocr.get_by_id(ocr_id)
    return templates.TemplateResponse("edit.html", {"request": request, "ocr": ocr})

@app.post("/edit/{ocr_id}")
async def update_ocr(
    ocr_id: int, 
    new_owner_name: str = Form(...),
    new_owner_address_main: str = Form(...),
    new_owner_address_street: str = Form(...),
    new_owner_address_number: str = Form(...),
    ):

    updated_at = datetime.now()

    ocr = Ocr.get_by_id(ocr_id)
    ocr.update(
        new_owner_name=new_owner_name,
        new_owner_address_main=new_owner_address_main,
        new_owner_address_street=new_owner_address_street,
        new_owner_address_number=new_owner_address_number,
        updated_at=updated_at,
    )
    return RedirectResponse(url=f"/list/{ocr.user_id}", status_code=303)


@app.delete("/api/ocr/{ocr_id}")
async def delete(ocr_id: int):
    ocr = Ocr.get_by_id(ocr_id)
    if not ocr:
        return Response(status_code=404)
    ocr.delete()
    return Response(status_code=204)
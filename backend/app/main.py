from fastapi import FastAPI, File, UploadFile, Request, Form, Response, HTTPException, Query
from typing import Optional, List
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openpyxl import Workbook
from io import BytesIO
from fastapi.templating import Jinja2Templates
from datetime import datetime
from zoneinfo import ZoneInfo
from app.model.Ocr import Ocr
import os

from app.ocr.vision import detect_text_from_image
from app.chatgpt.chatgpt import extract_structure_data_from_text

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

MAX_FILE_SIZE_MB = 5
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", "pdf"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get('/upload', response_class=HTMLResponse)
def get_upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload")
async def upload(new_owner_inkan: UploadFile = File(...)):
    ext = os.path.splitext(new_owner_inkan.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="許可されていないファイル形式です。")
    
    contents = await new_owner_inkan.read()
    file_size_mb = len(contents) / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"ファイルサイズが大きすぎます。(最大{MAX_FILE_SIZE_MB}まで)")
    
    ocr_text = detect_text_from_image(contents)
    structured_data = extract_structure_data_from_text(
        ocr_text, 
        document_type="new_owner_inkan"
        )
    
    ocr_record = Ocr.create(
            user_id=1,
            new_owner_name=structured_data.get("new_owner_name"),
            new_owner_address_main=structured_data.get("new_owner_address_main"),
            new_owner_address_street=structured_data.get("new_owner_address_street"),
            new_owner_address_number=structured_data.get("new_owner_address_number"),
            raw_text=ocr_text,
            created_at=datetime.now(ZoneInfo('Asia/Tokyo'))
        )
    
    return {
        "ok": True,
        "saved_id": ocr_record.id,
        "size_mb": round(file_size_mb, 2),
        "filename": new_owner_inkan.filename,
    }

@app.get('/api/ocr')
def api_get_ocr(user_id: int = Query(...)) -> List[dict]:
    ocrs = Ocr.get_by_user(user_id=user_id)
    result = []
    for ocr in ocrs:
        result.append({
            "id": ocr.id,
            "new_owner_name": ocr.new_owner_name,
            "new_owner_address_main": ocr.new_owner_address_main,
            "new_owner_address_street": ocr.new_owner_address_street,
            "new_owner_address_number": ocr.new_owner_address_number,
            "created_at": ocr.created_at,
            "updated_at": ocr.updated_at,
        })
    return result

# 編集
@app.get("/api/ocr/{ocr_id}")
def get_edit_list(ocr_id: int):
    ocr = Ocr.get_by_id(ocr_id)
    if not ocr:
        raise HTTPException(status_code=404, dtail="Not found")
    return {
        "id": ocr.id,
        "new_owner_name": ocr.new_owner_name,
        "new_owner_address_main": ocr.new_owner_address_main,
        "new_owner_address_street": ocr.new_owner_address_street,
        "new_owner_address_number": ocr.new_owner_address_number,
    }

@app.put("/api/ocr/{ocr_id}")
async def update_ocr(
    ocr_id: int, 
    new_owner_name: str = Form(...),
    new_owner_address_main: str = Form(...),
    new_owner_address_street: str = Form(...),
    new_owner_address_number: str = Form(...),
    ):

    updated_at = datetime.now(ZoneInfo('Asia/Tokyo'))

    ocr = Ocr.get_by_id(ocr_id)
    if not ocr:
        raise HTTPException(status_code=404, detail="Not found")
    
    ocr.update(
        new_owner_name=new_owner_name,
        new_owner_address_main=new_owner_address_main,
        new_owner_address_street=new_owner_address_street,
        new_owner_address_number=new_owner_address_number,
        updated_at=updated_at,
    )
    return {"message": "updated"}


@app.delete("/api/ocr/{ocr_id}")
async def delete(ocr_id: int):
    ocr = Ocr.get_by_id(ocr_id)
    if not ocr:
        return Response(status_code=404)
    ocr.delete()
    return Response(status_code=204)

@app.post("/export")
async def export_select_ocr(ocr_ids: List[int] = Form(...)):
    wb = Workbook()
    ws = wb.active
    ws.title = "OCR出力"

    ws.append(["ID", "新所有者名", "新所有者住所", "新所有者丁目", "新所有者番地"])

    for ocr_id in ocr_ids:
        ocr = Ocr.get_by_id(ocr_id)
        if ocr:
            ws.append([
                ocr.id,
                ocr.new_owner_name,
                ocr.new_owner_address_main,
                ocr.new_owner_address_street,
                ocr.new_owner_address_number,
            ])
    
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"{datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y%m%d_%H%M%S')}.xlsx"

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
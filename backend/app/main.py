from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import base64
import requests
import json
from app import settings

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get('/upload', response_class=HTMLResponse)
def get_upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post('/upload')
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    encoded_image = base64.b64encode(contents).decode("utf-8")

    request_data = {
        "requests": [
            {
                "image": {"content": encoded_image},
                "features": [{"type": "TEXT_DETECTION"}]
            }
        ]
    }

    endpoint_url = f"https://vision.googleapis.com/v1/images:annotate?key={settings.API_KEY}"

    response = requests.post(endpoint_url, json=request_data)

    if response.status_code == 200:
        response_data = response.json()
        try:
            detected_text = response_data["responses"][0]["textAnnotations"][0]["description"]
            print(detected_text)
        except (KeyError, IndexError):
            print("テキストが検出されませんでした。")
    else:
        print(f"エラーが発生しました。ステータスコード:{response.status_code}")
        print(response.text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
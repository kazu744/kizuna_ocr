import base64
import requests
from app import settings

def detect_text_from_image(contents: bytes) -> str:
    encoded_image = base64.b64encode(contents).decode("utf-8")

    request_data = {
        "requests": [
            {
                "image": {"content": encoded_image},
                "features": [{"type": "TEXT_DETECTION"}]
            }
        ]
    }

    endpoint_url = f"https://vision.googleapis.com/v1/images:annotate?key={settings.VISION_API_KEY}"

    response = requests.post(endpoint_url, json=request_data)

    if response.status_code != 200:
        return f"エラー：{response.status_code}"

    try:
        response_data = response.json()
        return response_data["responses"][0]["textAnnotations"][0]["description"]
    except (KeyError, IndexError):
        return "テキストが検出されませんでした。"
from openai import OpenAI
import json
import re
from app import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def extract_structure_data_from_text(ocr_text) -> dict:
    messages = [
        {
            "role": "user",
            "content": f"""以下は新所有者の印鑑証明書のテキストです。 
            {ocr_text}
            「氏名」「住所」をそれぞれ抽出して、JSON形式で出力してください。  
            ・企業の場合は商号を取得してください。
            ・姓と名、または会社形態と会社名、会社名と会社形態の間は1文字空けてください。(例: 田中　太郎)  
            ・建物名は削除してください。(例: きずなマンション201号室 → 201)
            ・住所に含まれる「字」、それ以降の町名・小字も削除し、市区町村までにとどめてください。（例："六本木字岩部" → "六本木"）
            ・丁目はアラビア数字に変換してください。
            ・不明な部分はNULLにしてください。
            ・以下のjsonフォーマットにしてください：
            {{
                "new_owner_name": "田中　太郎", 
                "new_owner_address_main": "兵庫県姫路市香寺町", 
                "new_owner_address_street": "1", 
                "new_owner_address_number": "96-1-301"
            }}
            """
        }
    ]

    response = client.chat.completions.create(
        model = "gpt-4o",
        messages=messages
    )
    print("🧠 GPT出力:", response.choices[0].message.content)
    return extract_json_from_response(response.choices[0].message.content)

def extract_json_from_response(content: str) -> dict:
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        return json.loads(match.group())
    else:
        return {"error": "JSON not found in response"}
    

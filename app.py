import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, request, jsonify
from functools import lru_cache
import warnings

# 壓制棄用警告
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()
app = Flask(__name__)

# 配置 Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    system_instruction="專業 Tagalog 教練。回應 JSON: {words: [{word, pronunciation, english}], sentences: [], quiz: []}",
    generation_config={
        "temperature": 0.3,
        "top_p": 0.8,
        "max_output_tokens": 1500
    }
)

@lru_cache(maxsize=256)
def generate_lesson(level: str) -> dict:
    """生成結構化 Tagalog 課堂"""
    prompt = f"""
    CEFR {level} Tagalog 15分鐘課堂 (JSON):
    - 10 單字 (Tagalog, IPA 發音, 英文)
    - 5 句子 + 翻譯
    - 5 選擇題測驗
    格式: {{
        "words": [{{"word": "salamat", "pron": "/sɐ.lɐˈmat/", "english": "thank you"}}],
        "sentences": [{{"tagalog": "Kumusta ka?", "english": "How are you?"}}],
        "quiz": ["問題1?", "A) a B) b"]
    }}
    """
    try:
        response = model.generate_content(prompt)
        return {
            "success": True,
            "content": response.text,
            "tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/lesson/<level>', methods=['GET'])
def lesson(level):
    data = generate_lesson(level)
    return jsonify(data)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Tagalog API 運行中！"})

if __name__ == '__main__':
    print("啟動 Tagalog 學習 API...")
    app.run(debug=True, host='0.0.0.0', port=5000)

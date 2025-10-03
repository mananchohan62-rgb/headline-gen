
from flask import Flask, request, jsonify
import os
import requests

app = Flask(_name_)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

@app.route("/headline", methods=["POST"])
def generate_headline():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "Koi text provide nahi hua"}), 400

    prompt = f"""
    Aapko Urdu mein di gayi khabar ka ek chhota aur seedha headline banana hai.
    Headline zyada se zyada 12 lafzon ki honi chahiye.
    
    Khabar:
    {text}
    """

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 100
    }

    r = requests.post(OPENAI_URL, headers=headers, json=body)

    if r.status_code != 200:
        return jsonify({"error": "OpenAI se masla aya", "details": r.text}), 500

    content = r.json()["choices"][0]["message"]["content"].strip()
    return jsonify({"headline": content})

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)

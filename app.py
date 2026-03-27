import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__, template_folder='.') # عشان يقرأ الـ HTML من المجلد الرئيسي

# إعداد Gemini
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    # البرومبت اللي بيخلي النتايج "Senior Level"
    prompt = f"""
    أنت خبير تسويق رقمي. حلل المشروع: {data.get('name')}. 
    الوصف: {data.get('desc')}. الموقع: {data.get('loc')}.
    أعطني عناوين إبداعية، كلمات SEO حقيقية، وأفكار محتوى. 
    لا تكرر كلامي، بل أضف قيمة إبداعية.
    """
    response = model.generate_content(prompt)
    return jsonify({'result': response.text})

if __name__ == '__main__':
    app.run(debug=True)

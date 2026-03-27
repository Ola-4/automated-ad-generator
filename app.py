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
    import os
import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__, template_folder='.')

# إعداد مفتاح Gemini (تأكدي من إضافته في Secrets باسم GEMINI_API_KEY)
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    lang = data.get('language', 'en')
    
    # بناء برومبت احترافي يطلب النتائج بصيغة JSON عشان الـ JS يفهمها
    prompt = f"""
    You are a Senior Content Strategist. Analyze this project:
    Project: {data.get('project')}
    Description: {data.get('service')}
    Industry: {data.get('industry')}
    Location: {data.get('location')}
    Audience: {data.get('audience')}
    Target Language: {lang}

    Return the results ONLY as a JSON object with these keys:
    - primaryKeywords: [list of 10 keywords]
    - supportingKeywords: [list of 6 keywords]
    - slogans: [list of 10 slogans]
    - shortHeadlines: [list of 10 catchy short headlines]
    - longHeadlines: [list of 10 value-driven headlines]
    - descriptions: [list of 10 creative ad descriptions]
    - ctas: [list of 10 powerful CTA phrases]
    - contentIdeas: [list of 10 unique social media/blog ideas]

    Be creative, don't repeat the input, and think outside the box. 
    Output should be in {lang}.
    """

    try:
        response = model.generate_content(prompt)
        # تنظيف الرد من أي كلام زائد (Markdown) لضمان إنه JSON خالص
        cleaned_response = response.text.replace('```json', '').replace('```', '').strip()
        ai_data = json.loads(cleaned_response)
        
        return jsonify({'success': True, 'data': ai_data})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # للتشغيل المحلي، في السيرفر سيستخدم المنصة المناسبة
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

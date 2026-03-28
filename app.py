import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

# 1. إعدادات الشاشة الكاملة
st.set_page_config(layout="wide", page_title="Smart Ads & SEO Builder")

# 2. CSS لإلغاء الهوامش تماماً ومنع التقطيع
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .main .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
        iframe { width: 100% !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_ai_content(data):
    if not data or 'project' not in data: return None
    
    # برومبت ذكي يدعم اللهجات المحلية
    prompt = f"""
    Act as a Senior Marketing Expert. Project: '{data['project']}'.
    Industry: {data['industry']}. Country: {data['country']}. Language: {data['language']}.
    Target Audience: {data.get('audience', 'General')}.
    
    INSTRUCTION: If Arabic is selected, use the local dialect of {data['country']} for Slogans and Headlines.
    Return ONLY a JSON object with keys: primaryKeywords, slogans, shortHeadlines, descriptions.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.replace('```json', '').replace('```', '').strip()
    except: return None

# 4. قراءة الـ HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# 5. عرض الواجهة واستلام البيانات
user_input = components.html(html_code, height=2000, scrolling=True)

if user_input:
    with st.spinner("Gemini is crafting your strategy..."):
        ai_res = get_ai_content(user_input)
        if ai_res:
            # حقن النتائج وفك تعليقة الزرار
            final_html = html_code.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {ai_res};")
            components.html(final_html, height=2000, scrolling=True)

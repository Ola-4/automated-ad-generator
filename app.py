import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

st.set_page_config(layout="wide", page_title="Smart Ads Builder")

# تصفير الهوامش تماماً
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .main .block-container { padding: 0 !important; max-width: 100% !important; }
        iframe { width: 100% !important; border: none !important; min-height: 100vh; }
    </style>
    """, unsafe_allow_html=True)

# إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_ai_content(data):
    # حماية من الـ TypeError: التأكد أن المدخلات ليست None وتحتوي على البيانات
    if not data or not isinstance(data, dict) or 'project' not in data:
        return None
    
    prompt = f"""
    As a Senior Content Developer, create a marketing strategy for:
    Project: {data['project']}, Industry: {data['industry']}, 
    Target Country: {data['country']}, Language: {data['language']}.
    Target Audience: {data.get('audience', 'General')}.
    
    CRITICAL: If the language is Arabic, use the local dialect of {data['country']} for Slogans and Headlines.
    Return ONLY a JSON object with keys: primaryKeywords, slogans, shortHeadlines, descriptions.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.replace('```json', '').replace('```', '').strip()
    except:
        return None

# قراءة الـ HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# عرض الواجهة (زودنا الارتفاع لـ 2000 لمنع القطع)
user_input = components.html(html_code, height=2000, scrolling=True)

# تنفيذ الـ AI فقط إذا ضغط المستخدم على زر Generate (يعني الـ user_input مش None)
if user_input and 'project' in user_input:
    with st.spinner("AI is thinking..."):
        ai_res = get_ai_content(user_input)
        if ai_res:
            final_html = html_code.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {ai_res};")
            components.html(final_html, height=2000, scrolling=True)

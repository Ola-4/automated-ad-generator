import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

st.set_page_config(layout="wide")

# الربط مع Gemini باستخدام Secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_gemini_content(info):
    prompt = f"Create a marketing strategy for {info['project']} in {info['industry']}. Language: {info['language']}. Return ONLY JSON with keys: primaryKeywords (list), slogans (list)."
    response = model.generate_content(prompt)
    return response.text.replace('```json', '').replace('```', '').strip()

# تحميل ملف الـ HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# عرض الواجهة واستلام البيانات
user_input = components.html(html_code, height=1000, scrolling=True)

if user_input:
    result = get_gemini_content(user_input)
    # إعادة إرسال النتيجة للـ HTML لعرضها
    components.html(html_code, height=1000, spec={"ai_output": result})

import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

st.set_page_config(layout="wide", page_title="Smart Ads Builder")

# إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_ai_content(data):
    if not data or 'project' not in data: return None
    prompt = f"Create a marketing strategy for {data['project']} targeting {data.get('audience', 'general audience')} in {data.get('language', 'ar')}. Return ONLY a JSON object with keys: primaryKeywords, slogans, shortHeadlines, descriptions."
    try:
        response = model.generate_content(prompt)
        return response.text.replace('```json', '').replace('```', '').strip()
    except: return None

# قراءة الـ HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# استلام المدخلات
user_input = components.html(html_code, height=1500)

# إذا ضغط المستخدم على الزرار وأرسل بيانات
if user_input:
    ai_res = get_ai_content(user_input)
    if ai_res:
        # حقن النتيجة في الـ HTML وإعادة عرضه فوراً لفك التعليقة
        new_html = html_code.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {ai_res};")
        components.html(new_html, height=1500)
    else:
        st.error("Gemini failed to respond. Please try again.")

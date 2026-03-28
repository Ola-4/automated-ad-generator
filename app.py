import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

st.set_page_config(layout="wide", page_title="Smart Content Builder")

# ذاكرة حفظ النتائج
if 'ai_results' not in st.session_state:
    st.session_state.ai_results = ""

# إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_ai_content(data):
    prompt = f"""
    Act as a Creative Director. Project: {data['project']}, Industry: {data['industry']}, 
    Language: {data['language']}. Audience: {data.get('audience', '')}.
    If Arabic, use Sudanese dialect if appropriate.
    Return ONLY a JSON with keys: primaryKeywords, slogans, shortHeadlines, descriptions.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.replace('```json', '').replace('```', '').strip()
    except: return None

# قراءة الواجهة
with open("index.html", "r", encoding="utf-8") as f:
    html_template = f.read()

# حقن النتائج لو موجودة
final_html = html_template
if st.session_state.ai_results:
    final_html = html_template.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {st.session_state.ai_results};")

# عرض الواجهة
user_input = components.html(final_html, height=1000, scrolling=True)

# معالجة الضغط
if user_input and isinstance(user_input, dict) and user_input.get('project'):
    res = get_ai_content(user_input)
    if res:
        st.session_state.ai_results = res
        st.rerun()

import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

st.set_page_config(layout="wide", page_title="Smart Ads Builder")

# 1. تهيئة الذاكرة (Session State)
if 'ai_results' not in st.session_state:
    st.session_state.ai_results = None

# إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_ai_content(data):
    if not data or not isinstance(data, dict) or not data.get('project'):
        return None
    
    prompt = f"""
    Create a marketing strategy for: Project: {data['project']}, Industry: {data['industry']}, 
    Country: {data['country']}, Language: {data['language']}.
    Return ONLY a JSON object with: primaryKeywords, slogans, shortHeadlines, descriptions.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.replace('```json', '').replace('```', '').strip()
    except:
        return None

# 2. قراءة الـ HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# 3. إذا كان عندنا نتائج قديمة في الذاكرة، نحقنها في الـ HTML قبل العرض
current_html = html_code
if st.session_state.ai_results:
    current_html = html_code.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {st.session_state.ai_results};")

# 4. عرض الواجهة
user_input = components.html(current_html, height=1200, scrolling=True)

# 5. معالجة الضغطة الجديدة
if user_input and isinstance(user_input, dict) and user_input.get('project'):
    # نتأكد إننا مش بنعيد نفس الطلب لو النتائج موجودة فعلاً
    res = get_ai_content(user_input)
    if res:
        st.session_state.ai_results = res
        st.rerun() # إعادة تشغيل الصفحة فوراً لحقن النتائج الجديدة

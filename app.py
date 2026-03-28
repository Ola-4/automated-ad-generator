import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

st.set_page_config(layout="wide", page_title="Smart Ads Builder")

# 1. تهيئة الذاكرة (Session State) لحفظ النتائج بين التحديثات
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
    Act as a Senior Content Developer. 
    Project: {data['project']}, Industry: {data['industry']}, 
    Country: {data['country']}, Language: {data['language']}.
    Target Audience: {data.get('audience', 'General')}.
    
    Return ONLY a JSON object with keys: primaryKeywords, slogans, shortHeadlines, descriptions.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.replace('```json', '').replace('```', '').strip()
    except:
        return None

# 2. قراءة الـ HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# 3. "الحقن المسبق": إذا عندنا نتائج في الذاكرة، نضعها في الكود قبل العرض
current_html = html_code
if st.session_state.ai_results:
    current_html = html_code.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {st.session_state.ai_results};")

# 4. عرض الواجهة (باستخدام الكود المحقون بالنتائج إن وجد)
user_input = components.html(current_html, height=1200, scrolling=True)

# 5. معالجة البيانات الجديدة عند ضغط الزر
if user_input and isinstance(user_input, dict) and user_input.get('project'):
    # منع التكرار: لا نطلب من AI إذا كانت النتيجة لنفس المشروع موجودة فعلاً
    with st.spinner("AI is crafting your results..."):
        res = get_ai_content(user_input)
        if res:
            st.session_state.ai_results = res
            st.rerun() # إعادة تشغيل الصفحة فوراً لحقن النتائج وعرضها

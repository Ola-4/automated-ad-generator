import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

st.set_page_config(layout="wide")

# تثبيت النتائج في الذاكرة
if 'final_data' not in st.session_state:
    st.session_state.final_data = ""

api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_ai(data):
    prompt = f"Marketing for {data['project']} in {data['industry']}. Country: {data['country']}. Language: {data['language']}. Audience: {data.get('audience', '')}. Return JSON only with: primaryKeywords, slogans, shortHeadlines, descriptions."
    try:
        res = model.generate_content(prompt)
        return res.text.replace('```json', '').replace('```', '').strip()
    except: return None

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# السحر هنا: حقن البيانات من الذاكرة في الـ HTML قبل العرض
if st.session_state.final_data:
    html = html.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {st.session_state.final_data};")

# عرض الواجهة
ui_return = components.html(html, height=1200, scrolling=True)

# إذا ضغطتي Generate والبيانات وصلت
if ui_return and isinstance(ui_return, dict) and 'project' in ui_return:
    if ui_return.get('project'):
        with st.spinner("Wait..."):
            result = get_ai(ui_return)
            if result:
                st.session_state.final_data = result
                st.rerun() # إعادة التشغيل لعرض البيانات المحقونة

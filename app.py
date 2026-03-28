import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

# 1. تفعيل وضع الشاشة الكاملة
st.set_page_config(layout="wide", page_title="Smart Ads & SEO Builder")

# 2. كود سحري لإلغاء هوامش Streamlit الافتراضية
st.markdown("""
    <style>
    .main .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        border: none !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_ai_content(data):
    # برومبت متطور لنتائج دقيقة
    prompt = f"As a Senior Content Developer, create a marketing strategy for {data['project']} in {data['industry']} language: {data['language']}. Return ONLY a JSON with keys: primaryKeywords, supportingKeywords, slogans, shortHeadlines, longHeadlines, descriptions, ctas, contentIdeas."
    response = model.generate_content(prompt)
    return response.text.replace('```json', '').replace('```', '').strip()

# 4. قراءة وعرض ملف الـ HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# استلام المدخلات من الواجهة
user_input = components.html(html_code, height=1800, scrolling=True)

# إذا وصلت بيانات من زر الـ Generate
if user_input:
    with st.spinner("Gemini is working..."):
        try:
            ai_res = get_ai_content(user_input)
            # إعادة إرسال النتيجة للواجهة
            components.html(html_code.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {ai_res};"), height=1800)
        except Exception as e:
            st.error(f"Error: {e}")

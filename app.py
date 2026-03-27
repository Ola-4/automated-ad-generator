import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
import json

# 1. إعداد الصفحة (عشان التصميم ياخد المساحة كاملة)
st.set_page_config(layout="wide", page_title="Smart Ads Builder")

# 2. إعداد Gemini
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("⚠️ يرجى إضافة GEMINI_API_KEY في الإعدادات!")

# 3. دالة معالجة الطلبات (الذكاء)
def get_ai_response(data):
    prompt = f"""
    Analyze as a Senior Content Strategist:
    Project: {data.get('project')}, Industry: {data.get('industry')}, Language: {data.get('language')}
    Return a JSON with: primaryKeywords, supportingKeywords, slogans, shortHeadlines, longHeadlines, descriptions, ctas, contentIdeas.
    Output must be in {data.get('language')}.
    """
    response = model.generate_content(prompt)
    return response.text.replace('```json', '').replace('```', '').strip()

# 4. عرض تصميمك الرهيب (HTML)
# هنا بنقرأ ملف الـ index.html بتاعك
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # عرض الـ HTML كـ Component في Streamlit
    components.html(html_code, height=1200, scrolling=True)
except FileNotFoundError:
    st.error("ملف index.html غير موجود في الـ GitHub!")

# ملاحظة: عشان الزراير تشتغل، حنحتاج تعديل بسيط في الـ JS اللي جوه الـ HTML 
# بس جربي ترفعي الـ app.py ده الأول وشوفي هل التصميم ظهر؟

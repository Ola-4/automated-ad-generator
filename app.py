import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

# 1. تفعيل وضع العرض الكامل
st.set_page_config(layout="wide", page_title="Smart Ads Builder")

# 2. الكود السحري لمسح حواف Streamlit تماماً
st.markdown("""
    <style>
        /* إخفاء الهيدر ومساحات التحميل */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* إجبار الحاوية الرئيسية تأخذ 100% من العرض */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
        }
        
        /* إلغاء المسافات بين العناصر */
        [data-testid="stVerticalBlock"] {
            padding: 0 !important;
            gap: 0 !important;
        }
        
        /* جعل الـ iframe يملأ الشاشة */
        iframe {
            width: 100% !important;
            border: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد Gemini (تأكدي من الـ Secrets)
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_ai_content(data):
    prompt = f"Analyze: {data['project']}, Industry: {data['industry']}. Return JSON with: primaryKeywords, slogans, shortHeadlines, descriptions."
    response = model.generate_content(prompt)
    return response.text.replace('```json', '').replace('```', '').strip()

# 4. عرض الـ HTML بمساحة عملاقة
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# هنا بنخلي الـ height كبير جداً عشان نضمن إنه يغطي كل التصميم
user_input = components.html(html_code, height=1800)

if user_input:
    # لما المستخدم يضغط Generate، بنعرض النتائج
    result = get_ai_content(user_input)
    components.html(html_code, height=1800, spec={"ai_output": result})

import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

# 1. إعداد الصفحة بأقصى عرض ممكن
st.set_page_config(layout="wide", page_title="Smart Ads & SEO Builder")

# 2. كود CSS جبار لمسح كل هوامش Streamlit وجعل الـ Iframe مالي الشاشة
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #root > div:nth-child(1) > div > div > div > div > section > div {padding: 0;}
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
        }
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_ai_content(data):
    # حماية: لو البيانات ناقصة ما يشتغلش
    if not data or 'project' not in data:
        return None
    
    prompt = f"Create marketing strategy for {data['project']}, Industry: {data['industry']}. Return ONLY JSON with keys: primaryKeywords (list), slogans (list), shortHeadlines (list), descriptions (list)."
    try:
        response = model.generate_content(prompt)
        # تنظيف الرد من أي علامات Markdown
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return clean_text
    except Exception as e:
        return json.dumps({"error": str(e)})

# 4. قراءة ملف الـ HTML
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
except FileNotFoundError:
    st.error("ملف index.html غير موجود!")
    st.stop()

# 5. تشغيل المكون وعلاج الـ TypeError
# وضعنا القيمة الافتراضية None لمنع الخطأ في أول تشغيل
user_input = components.html(html_code, height=1200)

if user_input is not None:
    # هنا نتأكد إن البيانات جات فعلاً من زر الـ Generate
    with st.spinner("AI is thinking..."):
        ai_res = get_ai_content(user_input)
        if ai_res:
            # إعادة حقن النتائج داخل الـ HTML وعرضها فوراً
            final_html = html_code.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {ai_res};")
            components.html(final_html, height=1200)

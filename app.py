import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

# 1. إعدادات الشاشة الكاملة (Wide Mode)
st.set_page_config(
    layout="wide", 
    page_title="Smart Ads & SEO Builder",
    initial_sidebar_state="collapsed"
)

# 2. كود CSS لتصفير الهوامش تماماً ومنع أي مسافات بيضاء
st.markdown("""
    <style>
        /* إخفاء العناصر الافتراضية لستريمليت */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #root > div:nth-child(1) > div > div > div > div > section > div {padding: 0;}
        
        /* إجبار الحاوية الرئيسية على ملء الشاشة */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
        }
        
        /* تنسيق الـ Iframe ليكون مريحاً في العرض */
        iframe {
            width: 100% !important;
            border: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد Gemini API
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.warning("يرجى إضافة GEMINI_API_KEY في الإعدادات (Secrets)")

def get_ai_content(data):
    # حماية للتأكد من وجود بيانات حقيقية
    if not data or not isinstance(data, dict) or 'project' not in data:
        return None
    
    prompt = f"""
    As a Senior Content Developer, create a marketing strategy for:
    Project: {data.get('project')}
    Industry: {data.get('industry')}
    Target Audience: {data.get('audience', 'General')}
    Language: {data.get('language', 'en')}
    
    Return ONLY a valid JSON object with these keys:
    "primaryKeywords", "slogans", "shortHeadlines", "descriptions"
    (All values should be lists of strings)
    """
    try:
        response = model.generate_content(prompt)
        # تنظيف الرد من أي زيادات
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return clean_text
    except Exception as e:
        return json.dumps({"error": str(e)})

# 4. تحميل وعرض الواجهة
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
except FileNotFoundError:
    st.error("ملف index.html غير موجود في المستودع!")
    st.stop()

# عرض المكون مع زيادة الارتفاع وتفعيل السكرول لمنع القطع
# الارتفاع 2500 يضمن ظهور كل الكروت والنتائج بوضوح
user_input = components.html(html_code, height=2500, scrolling=True)

# 5. معالجة الطلب عند ضغط زر Generate
if user_input:
    with st.spinner("جاري تحليل البيانات بواسطة Gemini..."):
        ai_res = get_ai_content(user_input)
        if ai_res:
            # دمج النتائج داخل كود الـ HTML وإعادة عرضه
            final_html = html_code.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {ai_res};")
            components.html(final_html, height=2500, scrolling=True)

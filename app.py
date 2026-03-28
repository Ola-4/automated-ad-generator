import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import json

st.set_page_config(layout="wide", page_title="Content Generator")

# ذاكرة النتائج
if 'final_res' not in st.session_state:
    st.session_state.final_res = None

# إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def process_ai(data):
    # برومبت ذكي يفهم اللغة المختارة
    lang_instruction = "Write in Arabic (Sudanese dialect where appropriate)" if data['language'] == 'ar' else "Write in professional English"
    
    prompt = f"""
    Act as a Content Strategist. 
    Project: {data['project']}, Industry: {data['industry']}, Audience: {data['audience']}.
    {lang_instruction}.
    Return ONLY a JSON object: 
    {{"keywords": ["list"], "slogans": ["list"], "headlines": ["list"], "descriptions": ["list"]}}
    """
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text.replace('```json', '').replace('```', '').strip())
    except: return None

# عرض واجهة الإدخال
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

user_data = components.html(html_code, height=550)

# عند استلام البيانات
if user_data and isinstance(user_data, dict) and user_data.get('project'):
    with st.spinner("⏳ جاري تحضير المحتوى الإبداعي..."):
        result = process_ai(user_data)
        if result:
            st.session_state.final_res = result

# عرض النتائج في "Cards" أنيقة من Streamlit
if st.session_state.final_res:
    res = st.session_state.final_res
    st.success("✅ تم توليد المحتوى بنجاح!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🔎 كلمات البحث (SEO)")
        st.write(", ".join(res['keywords']))
        
        st.info("✨ الشعارات المقترحة")
        for s in res['slogans']: st.markdown(f"**- {s}**")

    with col2:
        st.info("📣 عناوين جذابة")
        for h in res['headlines']: st.markdown(f"**- {h}**")
            
        st.info("📝 الأوصاف التسويقية")
        for d in res['descriptions']: st.markdown(f"> {d}")

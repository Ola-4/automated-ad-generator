import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import json

st.set_page_config(layout="wide", page_title="Hakaweena Content Builder")

# ذاكرة لحفظ النتائج عشان ما تختفي
if 'my_results' not in st.session_state:
    st.session_state.my_results = None

# إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_content(data):
    # برومبت يركز على اللهجة السودانية لو اللغة عربية
    style = "Sudanese dialect" if data['language'] == 'ar' else "Professional English"
    prompt = f"Marketing content for {data['project']} in {data['industry']}. Language: {data['language']} ({style}). Return ONLY JSON: {{\"k\":[\"keywords\"], \"s\":[\"slogans\"], \"h\":[\"headlines\"], \"d\":[\"descriptions\"]}}"
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text.replace('```json', '').replace('```', '').strip())
    except: return None

# عرض واجهة الإدخال (index.html)
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# هنا بنعرض الواجهة اللي بتكتبي فيها
input_data = components.html(html_code, height=500)

# أول ما تضغطي الزرار وتوصل البيانات
if input_data and isinstance(input_data, dict) and input_data.get('project'):
    with st.spinner("⏳ بنجهز ليك الإبداع..."):
        res = get_content(input_data)
        if res:
            st.session_state.my_results = res

# **المكان اللي حيتولد فيه المحتوى** (تحت الواجهة مباشرة)
if st.session_state.my_results:
    res = st.session_state.my_results
    st.markdown("---")
    st.balloons() # احتفال بسيط بالنجاح
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🔎 كلمات البحث (SEO)", expanded=True):
            st.write(", ".join(res['k']))
        with st.expander("✨ الشعارات (Slogans)", expanded=True):
            for s in res['s']: st.info(s)

    with col2:
        with st.expander("📣 العناوين الجذابة", expanded=True):
            for h in res['h']: st.warning(h)
        with st.expander("📝 الأوصاف التسويقية", expanded=True):
            for d in res['d']: st.success(d)

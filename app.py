import streamlit as st
import google.generativeai as genai
import json

# إعداد الصفحة
st.set_page_config(layout="centered", page_title="Hakaweena AI")

# تنسيق جمالي بسيط
st.markdown("""
    <style>
    .stButton>button { width: 100%; background: linear-gradient(135deg, #7c3aed, #06b6d4); color: white; height: 3em; border-radius: 10px; font-weight: bold; border: none; }
    .res-box { background: #1e293b; padding: 15px; border-radius: 10px; border-right: 5px solid #7c3aed; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("إعدادات هكاوينا ✨")

# المدخلات (أدوات Streamlit الرسمية مستحيل تضرب)
project_name = st.text_input("اسم المشروع", placeholder="Hakaweena...")
col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("اللغة", ["العربية (سوداني)", "English"])
with col2:
    industry = st.selectbox("المجال", ["Podcast", "Cooking", "SaaS", "Real Estate"])

audience = st.text_area("الجمهور المستهدف", placeholder="الناس المهتمة بالثقافة...")

generate_btn = st.button("✨ توليد المحتوى الآن")

# إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

if generate_btn:
    if not project_name:
        st.warning("يا علا، اكتبي اسم المشروع أولاً!")
    else:
        with st.spinner("⏳ جاري تحضير الإبداع..."):
            prompt = f"Marketing for {project_name} in {industry}. Language: {lang}. Audience: {audience}. Return ONLY JSON: {{\"k\":[\"keywords\"], \"s\":[\"slogans\"], \"h\":[\"headlines\"], \"d\":[\"descriptions\"]}}"
            try:
                response = model.generate_content(prompt)
                res = json.loads(response.text.replace('```json', '').replace('```', '').strip())
                
                st.success("✅ تم توليد المحتوى!")
                
                # عرض النتائج في Tabs أنيقة
                tab1, tab2, tab3, tab4 = st.tabs(["🔎 SEO", "✨ الشعارات", "📣 العناوين", "📝 الأوصاف"])
                
                with tab1:
                    st.write(", ".join(res['k']))
                with tab2:
                    for s in res['s']: st.markdown(f'<div class="res-box">{s}</div>', unsafe_allow_html=True)
                with tab3:
                    for h in res['h']: st.markdown(f'<div class="res-box">{h}</div>', unsafe_allow_html=True)
                with tab4:
                    for d in res['d']: st.info(d)
            except Exception as e:
                st.error("عذراً، حدث خطأ في الاتصال. تأكدي من مفتاح API وجربي ثانية.")

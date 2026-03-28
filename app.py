import streamlit as st
import google.generativeai as genai
import json

# إعداد الصفحة وتنسيقها
st.set_page_config(layout="centered", page_title="Hakaweena AI Builder")

# تنسيق الألوان يدوياً عشان يطلع شكل احترافي
st.markdown("""
    <style>
    .stButton>button { width: 100%; background: linear-gradient(135deg, #7c3aed, #06b6d4); color: white; border: none; padding: 15px; border-radius: 10px; font-weight: bold; }
    .result-card { background: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #7c3aed; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("إعدادات هكاوينا ✨")

# المدخلات باستخدام أدوات Streamlit الأصلية (أضمن وأسرع)
with st.container():
    project_name = st.text_input("اسم المشروع", placeholder="مثلاً: هكاوينا")
    col_a, col_b = st.columns(2)
    with col_a:
        lang = st.selectbox("اللغة", ["العربية (لهجة سودانية)", "English"])
    with col_b:
        industry = st.selectbox("المجال", ["بودكاست", "طبخ", "عقارات", "تجارة إلكترونية"])
    
    audience = st.text_area("الجمهور المستهدف", placeholder="الناس المهتمة بالثقافة والتاريخ...")
    
    generate_btn = st.button("✨ توليد المحتوى الآن")

# إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

if generate_btn:
    if not project_name:
        st.error("يا علا، اكتبي اسم المشروع أولاً!")
    else:
        with st.spinner("⏳ جاري استخراج الإبداع..."):
            prompt = f"Marketing content for {project_name} in {industry}. Language: {lang}. Audience: {audience}. Return JSON: {{\"k\":[\"keywords\"], \"s\":[\"slogans\"], \"h\":[\"headlines\"], \"d\":[\"descriptions\"]}}"
            try:
                response = model.generate_content(prompt)
                res = json.loads(response.text.replace('```json', '').replace('```', '').strip())
                
                # عرض النتائج بشكل مرتب جداً
                st.success("✅ النتائج جاهزة!")
                
                tabs = st.tabs(["🔎 SEO", "✨ الشعارات", "📣 العناوين", "📝 الأوصاف"])
                
                with tabs[0]:
                    st.write(", ".join(res['k']))
                with tabs[1]:
                    for s in res['s']: st.markdown(f'<div class="result-card">{s}</div>', unsafe_allow_html=True)
                with tabs[2]:
                    for h in res['h']: st.markdown(f'<div class="result-card">{h}</div>', unsafe_allow_html=True)
                with tabs[3]:
                    for d in res['d']: st.info(d)
            except:
                st.error("حصل خطأ في الاتصال بالذكاء الاصطناعي، جربي مرة ثانية.")

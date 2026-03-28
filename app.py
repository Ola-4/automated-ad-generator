import streamlit as st
import google.generativeai as genai
import json

# 1. إعداد الصفحة وتنسيقها لتكون مريحة للعين
st.set_page_config(layout="wide", page_title="AI Content Strategist")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select {
        background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important;
    }
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #7c3aed, #06b6d4);
        color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px;
    }
    .result-card { background: #1e293b; padding: 15px; border-radius: 10px; border-left: 5px solid #7c3aed; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 محرك صناعة المحتوى و SEO")
st.info("أدخلي بيانات أي مشروع للحصول على خطة محتوى فورية.")

# 2. إعداد Gemini (تأكدي من وجود المفتاح في Secrets)
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

# 3. واجهة المدخلات (مباشرة وبدون تعقيد HTML)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("اسم المشروع", placeholder="مثلاً: هكاوينا أو مشروع جديد...")
        industry = st.selectbox("المجال", ["بودكاست", "تقنية", "عقارات", "طبخ", "تعليم", "تجارة إلكترونية"])
    with col2:
        lang = st.selectbox("اللغة", ["العربية", "English"])
        country = st.text_input("الدولة المستهدفة", value="Sudan")

    audience = st.text_area("الجمهور المستهدف", placeholder="اوصفي جمهورك هنا...")
    
    generate = st.button("توليد المحتوى ✨")

# 4. معالجة البيانات وعرضها
if generate:
    if not p_name:
        st.error("لازم تكتبي اسم المشروع يا علا!")
    else:
        with st.spinner("⏳ جاري استخراج النتائج..."):
            prompt = f"""
            Act as a Senior SEO Specialist. Project: {p_name}, Industry: {industry}, Language: {lang}.
            Target Audience: {audience}.
            Return ONLY a JSON object with: 
            "k": ["5 keywords"], "s": ["3 slogans"], "h": ["3 headlines"], "d": ["2 descriptions"].
            """
            try:
                response = model.generate_content(prompt)
                res = json.loads(response.text.replace('```json', '').replace('```', '').strip())
                
                st.divider()
                st.success(f"نتائج مشروع: {p_name}")
                
                # عرض النتائج في تبويبات واضحة
                tab1, tab2, tab3 = st.tabs(["🔎 SEO & Keywords", "✨ الشعارات", "📣 العناوين والأوصاف"])
                
                with tab1:
                    st.write("### كلمات البحث المستهدفة")
                    st.write(", ".join(res['k']))
                
                with tab2:
                    for s in res['s']:
                        st.markdown(f'<div class="result-card">{s}</div>', unsafe_allow_html=True)
                
                with tab3:
                    for h in res['h']:
                        st.write(f"**العنوان:** {h}")
                    st.divider()
                    for d in res['d']:
                        st.info(f"وصف SEO: {d}")
            except Exception as e:
                st.error("حصلت مشكلة في الاتصال بالذكاء الاصطناعي. اتأكدي إن الـ API Key صحيحة.")

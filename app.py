import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(layout="wide", page_title="Professional Content Builder")

# تنسيق الواجهة لتناسب ذوقك كـ Content Developer
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        background-color: #1e293b; color: white; border-radius: 8px; border: 1px solid #334155;
    }
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #7c3aed, #06b6d4);
        color: white; border: none; padding: 12px; font-weight: bold; border-radius: 8px;
    }
    .info-card { background: #1e293b; padding: 15px; border-radius: 10px; border-left: 4px solid #06b6d4; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 محرك صناعة المحتوى الذكي")
st.write("أداة احترافية لتوليد خطط المحتوى، الـ SEO، والشعارات لأي مشروع.")

# إعداد Gemini
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

# واجهة المدخلات العامة (ليست محصورة بمشروع واحد)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("اسم المشروع / العلامة التجارية", placeholder="أدخلي اسم المشروع هنا...")
        industry = st.selectbox("مجال العمل", ["بودكاست", "تقنية/SaaS", "عقارات", "طبخ/أغذية", "تعليم", "تجارة إلكترونية", "أخرى"])
    with col2:
        target_country = st.selectbox("الدولة المستهدفة", ["Sudan", "Saudi Arabia", "UAE", "Egypt", "Global"])
        lang = st.selectbox("اللغة", ["العربية", "English"])

    audience = st.text_area("تفاصيل الجمهور المستهدف (Target Audience)", placeholder="مثلاً: الشباب المهتمين بالثقافة، أو أصحاب الشركات الناشئة...")
    
    generate = st.button("توليد الخطة التسويقية ✨")

if generate:
    if not p_name:
        st.warning("الرجاء إدخال اسم المشروع للمتابعة.")
    else:
        with st.spinner("جاري تحليل البيانات وتوليد المحتوى..."):
            # برومبت احترافي يركز على الـ SEO والتحويل (Conversion)
            prompt = f"""
            Act as a Senior SEO & Content Strategist. 
            Create a data-driven content plan for:
            Project: {p_name}, Industry: {industry}, Country: {target_country}, Language: {lang}.
            Target Audience: {audience}.
            Return ONLY a JSON object with: 
            "keywords": [5 SEO keywords], 
            "slogans": [3 creative slogans], 
            "headlines": [3 SEO-optimized headlines], 
            "descriptions": [2 meta descriptions].
            """
            try:
                response = model.generate_content(prompt)
                res = json.loads(response.text.replace('```json', '').replace('```', '').strip())
                
                st.success(f"تم تجهيز الخطة لمشروع: {p_name}")
                
                # عرض النتائج في أعمدة احترافية
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.subheader("🔎 SEO & Keywords")
                    st.write(", ".join(res['keywords']))
                    st.subheader("✨ Slogans")
                    for s in res['slogans']: st.markdown(f'<div class="info-card">{s}</div>', unsafe_allow_html=True)
                
                with res_col2:
                    st.subheader("📣 Headlines")
                    for h in res['headlines']: st.markdown(f'<div class="info-card">{h}</div>', unsafe_allow_html=True)
                    st.subheader("📝 Meta Descriptions")
                    for d in res['descriptions']: st.info(d)
            except:
                st.error("عذراً، حدث خطأ. تأكدي من إعدادات الـ API.")

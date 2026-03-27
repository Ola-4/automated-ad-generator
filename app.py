import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="AI Content Strategist", page_icon="🧠")

# الربط بـ Gemini (عشان النتايج تكون عبقرية مش تعبانة)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
else:
    st.warning("⚠️ بانتظار إضافة الـ API Key في الإعدادات لتفعيل الذكاء الكامل.")
    # لو مافي مفتاح، حنشغل نسخة تجريبية بسيطة
    model = None

st.title("🤖 مساعد التسويق الذكي")
st.write("أنا هنا عشان أحلل مشروعك وأديك أفكار حقيقية، مش بس أكرر كلامك!")

# المدخلات في الجنب
with st.sidebar:
    project_name = st.text_input("اسم المشروع")
    description = st.text_area("اشرحي لي فكرة المشروع (مثلاً: تطبيق قصص للأطفال)")
    location = st.text_input("الموقع المستهدف (مثلاً: السودان، السعودية)")
    generate_btn = st.button("توليد أفكار إبداعية")

# التنفيذ
if generate_btn and project_name and description:
    if model:
        with st.spinner("جاري التحليل الإبداعي..."):
            prompt = f"حلل المشروع التالي بذكاء: {project_name}. الوصف: {description}. الموقع: {location}. أعطني 3 عناوين إعلانية عاطفية، و5 كلمات SEO ذكية، وفكرة محتوى واحدة تجذب الجمهور."
            response = model.generate_content(prompt)
            st.success("إليك الاستراتيجية المقترحة:")
            st.markdown(response.text)
    else:
        st.info(f"نتايج تجريبية لـ {project_name}: العناوين والكلمات المفتاحية ستظهر هنا بمجرد ربط الـ API Key.")

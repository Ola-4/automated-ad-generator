import json

import streamlit as st

from google import genai



st.set_page_config(layout="wide", page_title="Professional Content Builder")



st.markdown("""

<style>

.main { background-color: #0f172a; }

.stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {

    background-color: #1e293b;

    color: white;

    border-radius: 8px;

    border: 1px solid #334155;

}

.stButton>button {

    width: 100%;

    background: linear-gradient(90deg, #7c3aed, #06b6d4);

    color: white;

    border: none;

    padding: 12px;

    font-weight: bold;

    border-radius: 8px;

}

.info-card {

    background: #1e293b;

    padding: 15px;

    border-radius: 10px;

    border-left: 4px solid #06b6d4;

    margin-bottom: 10px;

}

</style>

""", unsafe_allow_html=True)



st.title("🚀 محرك صناعة المحتوى الذكي")

st.write("أداة احترافية لتوليد خطط المحتوى، SEO، والشعارات لأي مشروع.")



api_key = st.secrets.get("GEMINI_API_KEY")



if not api_key:

    st.error("GEMINI_API_KEY is missing from Streamlit secrets.")

    st.stop()



client = genai.Client(api_key=api_key)



with st.container():

    col1, col2 = st.columns(2)



    with col1:

        p_name = st.text_input(

            "اسم المشروع / العلامة التجارية",

            placeholder="أدخلي اسم المشروع هنا..."

        )

        industry = st.selectbox(

            "مجال العمل",

            ["بودكاست", "تقنية/SaaS", "عقارات", "طبخ/أغذية", "تعليم", "تجارة إلكترونية", "أخرى"]

        )



    with col2:

        target_country = st.selectbox(

            "الدولة المستهدفة",

            ["Sudan", "Saudi Arabia", "UAE", "Egypt", "Global"]

        )

        lang = st.selectbox("اللغة", ["العربية", "English"])



    audience = st.text_area(

        "تفاصيل الجمهور المستهدف (Target Audience)",

        placeholder="مثلاً: الشباب المهتمين بالثقافة، أو أصحاب الشركات الناشئة..."

    )



    generate = st.button("توليد الخطة التسويقية ✨")



def extract_json(text: str) -> dict:

    text = text.strip()

    if text.startswith("```"):

        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)



if generate:

    if not p_name:

        st.warning("الرجاء إدخال اسم المشروع للمتابعة.")

    else:

        prompt = f"""

Act as a Senior SEO & Content Strategist.



Create a data-driven content plan for:

Project: {p_name}

Industry: {industry}

Country: {target_country}

Language: {lang}

Target Audience: {audience}



Return ONLY valid JSON with this exact structure:

{{

  "keywords": ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"],

  "slogans": ["slogan 1", "slogan 2", "slogan 3"],

  "headlines": ["headline 1", "headline 2", "headline 3"],

  "descriptions": ["description 1", "description 2"]

}}

"""



        with st.spinner("جاري تحليل البيانات وتوليد المحتوى..."):

            try:

                response = client.models.generate_content(

                    model="gemini-2.5-flash",

                    contents=prompt,

                )



                raw_text = response.text

                res = extract_json(raw_text)



                st.success(f"تم تجهيز الخطة لمشروع: {p_name}")



                res_col1, res_col2 = st.columns(2)



                with res_col1:

                    st.subheader("🔎 SEO & Keywords")

                    st.write(", ".join(res["keywords"]))



                    st.subheader("✨ Slogans")

                    for s in res["slogans"]:

                        st.markdown(

                            f'<div class="info-card">{s}</div>',

                            unsafe_allow_html=True

                        )



                with res_col2:

                    st.subheader("📣 Headlines")

                    for h in res["headlines"]:

                        st.markdown(

                            f'<div class="info-card">{h}</div>',

                            unsafe_allow_html=True

                        )



                    st.subheader("📝 Meta Descriptions")

                    for d in res["descriptions"]:

                        st.info(d)



            except Exception as e:

                st.error(f"حدث خطأ: {e}")

import json
import streamlit as st
from google import genai

st.set_page_config(layout="wide", page_title="Professional Content Builder")

st.markdown("""
<style>
.main {
    background-color: #0f172a;
}

/* General text */
html, body, [class*="css"] {
    color: #f8fafc;
}

/* Labels */
label, .stTextInput label, .stSelectbox label, .stTextArea label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
}

/* Select boxes */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
}

/* Placeholder text */
input::placeholder,
textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    color: white;
    border: none;
    padding: 12px;
    font-weight: bold;
    border-radius: 10px;
}

/* Result cards */
.info-card {
    background: #1e293b;
    color: #f8fafc;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #06b6d4;
    margin-bottom: 10px;
}

.small-card {
    background: #1e293b;
    color: #f8fafc;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
}

/* Success/info */
.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Smart Ads Generator")
st.write("أداة احترافية لتوليد خطط المحتوى، SEO، الشعارات، العناوين، والأفكار التسويقية.")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing from Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=api_key)


def get_country_tone(country: str, lang: str) -> str:
    if lang == "العربية":
        if country == "Egypt":
            return "Write in Arabic with a light Egyptian marketing tone. Keep it natural, catchy, and easy to understand. Avoid heavy slang."
        if country == "Saudi Arabia":
            return "Write in Arabic with a Saudi-friendly marketing tone. Keep it polished, modern, and audience-friendly."
        if country == "UAE":
            return "Write in Arabic with a UAE-friendly Gulf marketing tone. Keep it elegant, modern, and smooth."
        if country == "Sudan":
            return "Write in Arabic with a Sudan-friendly marketing tone. Keep it warm, simple, and relatable."
        return "Write in clear modern Arabic with a strong marketing tone."
    return "Write in polished marketing English adapted to the target country and audience."


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        p_name = st.text_input(
            "اسم المشروع / العلامة التجارية",
            placeholder="أدخلي اسم المشروع هنا..."
        )

        industry = st.selectbox(
            "مجال العمل",
            [
                "بودكاست",
                "تقنية/SaaS",
                "عقارات",
                "طبخ/أغذية",
                "تعليم",
                "تجارة إلكترونية",
                "صحة/عافية",
                "جمال",
                "رياضة",
                "أخرى"
            ]
        )

    with col2:
        target_country = st.selectbox(
            "الدولة المستهدفة",
            ["Egypt", "Saudi Arabia", "UAE", "Sudan", "Global"]
        )

        lang = st.selectbox("اللغة", ["العربية", "English"])

    audience = st.text_area(
        "تفاصيل الجمهور المستهدف (Target Audience)",
        placeholder="مثلاً: الشباب المهتمين بالثقافة، أو أصحاب الشركات الناشئة..."
    )

    seed_keywords = st.text_area(
        "الكلمات المفتاحية الأساسية (Seed Keywords)",
        placeholder="مثلاً: بودكاست, قصص, محتوى صوتي, ثقافة, إلهام"
    )

    generate = st.button("توليد الخطة التسويقية ✨")


if generate:
    if not p_name:
        st.warning("الرجاء إدخال اسم المشروع للمتابعة.")
    else:
        tone_instruction = get_country_tone(target_country, lang)

        prompt = f"""
Act as a Senior SEO & Content Strategist and high-conversion copywriter.

Project Name: {p_name}
Industry: {industry}
Target Country: {target_country}
Language: {lang}
Target Audience: {audience}
Seed Keywords: {seed_keywords}

Important writing instruction:
{tone_instruction}

Requirements:
- Make the output feel relevant to the target country.
- If the selected language is Arabic, adapt the wording style to the selected country.
- Use the seed keywords naturally.
- Keep the output marketing-focused, realistic, and usable.
- Avoid generic filler.
- Return ONLY valid JSON.

Return this exact JSON structure:
{{
  "keywords": ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"],
  "slogans": ["slogan 1", "slogan 2", "slogan 3"],
  "short_headlines": ["short 1", "short 2", "short 3", "short 4", "short 5"],
  "long_headlines": ["long 1", "long 2", "long 3", "long 4", "long 5"],
  "descriptions": ["description 1", "description 2", "description 3"],
  "ctas": ["cta 1", "cta 2", "cta 3", "cta 4"],
  "content_ideas": ["idea 1", "idea 2", "idea 3", "idea 4", "idea 5"]
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

                col_a, col_b = st.columns(2)

                with col_a:
                    st.subheader("🔎 SEO Keywords")
                    for k in res["keywords"]:
                        st.markdown(
                            f'<div class="small-card">{k}</div>',
                            unsafe_allow_html=True
                        )

                    st.subheader("✨ Slogans")
                    for s in res["slogans"]:
                        st.markdown(
                            f'<div class="info-card">{s}</div>',
                            unsafe_allow_html=True
                        )

                    st.subheader("🚀 CTA")
                    for c in res["ctas"]:
                        st.markdown(
                            f'<div class="small-card">{c}</div>',
                            unsafe_allow_html=True
                        )

                with col_b:
                    st.subheader("📣 Short Headlines")
                    for h in res["short_headlines"]:
                        st.markdown(
                            f'<div class="info-card">{h}</div>',
                            unsafe_allow_html=True
                        )

                    st.subheader("📢 Long Headlines")
                    for h in res["long_headlines"]:
                        st.markdown(
                            f'<div class="info-card">{h}</div>',
                            unsafe_allow_html=True
                        )

                st.subheader("📝 Descriptions")
                for d in res["descriptions"]:
                    st.info(d)

                st.subheader("💡 Content Ideas")
                for idea in res["content_ideas"]:
                    st.markdown(
                        f'<div class="small-card">{idea}</div>',
                        unsafe_allow_html=True
                    )

            except Exception as e:
                st.error(f"حدث خطأ: {e}")

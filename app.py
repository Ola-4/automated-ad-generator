import json
import re
import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai

st.set_page_config(layout="wide", page_title="Professional Content Builder")

st.markdown("""
<style>
.main {
    background:
        radial-gradient(circle at top left, rgba(124, 58, 237, 0.22), transparent 30%),
        radial-gradient(circle at top right, rgba(6, 182, 212, 0.18), transparent 28%),
        linear-gradient(135deg, #0f172a, #111827, #1e293b);
}

html, body, [class*="css"] {
    color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

label, .stTextInput label, .stSelectbox label, .stTextArea label {
    color: #e2e8f0 !important;
    font-weight: 700 !important;
}

.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border-radius: 12px !important;
    border: 1px solid #cbd5e1 !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border-radius: 12px !important;
    border: 1px solid #cbd5e1 !important;
}

input::placeholder,
textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    color: white;
    border: none;
    padding: 12px;
    font-weight: bold;
    border-radius: 12px;
    box-shadow: 0 10px 24px rgba(124, 58, 237, 0.25);
}

.info-card {
    background: linear-gradient(135deg, rgba(30,41,59,0.95), rgba(15,23,42,0.95));
    color: #f8fafc;
    padding: 15px;
    border-radius: 14px;
    border-left: 4px solid #06b6d4;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.06);
}

.small-card {
    background: linear-gradient(135deg, rgba(51,65,85,0.95), rgba(30,41,59,0.95));
    color: #f8fafc;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 8px;
    border: 1px solid rgba(255,255,255,0.06);
}

.stAlert {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing from Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=api_key)


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


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


def ui_text(lang: str) -> dict:
    if lang == "العربية":
        return {
            "page_title": "🚀 محرك صناعة المحتوى الذكي",
            "subtitle": "أداة احترافية لتوليد خطط المحتوى، SEO، الشعارات، العناوين، والأفكار التسويقية.",
            "project_label": "اسم المشروع / العلامة التجارية",
            "project_placeholder": "أدخلي اسم المشروع هنا...",
            "industry_label": "مجال العمل",
            "country_label": "الدولة المستهدفة",
            "audience_label": "تفاصيل الجمهور المستهدف",
            "audience_placeholder": "مثلاً: الشباب المهتمين بالثقافة، أو أصحاب الشركات الناشئة...",
            "seed_label": "الكلمات المفتاحية الأساسية",
            "seed_placeholder": "مثلاً: بودكاست, قصص, محتوى صوتي, ثقافة, إلهام",
            "url_label": "رابط الموقع أو الصفحة",
            "url_placeholder": "مثلاً: https://example.com",
            "button": "توليد الخطة التسويقية ✨",
            "warning_project": "الرجاء إدخال اسم المشروع للمتابعة.",
            "spinner": "جاري تحليل البيانات وتوليد المحتوى...",
            "success": "تم تجهيز الخطة لمشروع: ",
            "seo": "🔎 الكلمات المفتاحية SEO",
            "primary_keywords": "الكلمات المفتاحية الأساسية",
            "supporting_keywords": "الكلمات المفتاحية الداعمة",
            "meta_title": "عنوان الميتا",
            "meta_description": "وصف الميتا",
            "slogans": "✨ الشعارات",
            "short_headlines": "📣 العناوين القصيرة",
            "long_headlines": "📢 العناوين الطويلة",
            "descriptions": "📝 الوصف التسويقي",
            "ctas": "🚀 الدعوات لاتخاذ إجراء",
            "ideas": "💡 أفكار المحتوى",
            "url_ok": "تم التحقق من الرابط واستخدام محتواه لتحسين النتائج.",
            "url_bad": "تعذر قراءة الرابط. سيتم التوليد بدون محتوى الصفحة.",
            "url_invalid": "الرابط غير صالح. سيتم تجاهله."
        }
    return {
        "page_title": "🚀 Smart Content Builder",
        "subtitle": "A professional tool to generate SEO plans, slogans, headlines, descriptions, and marketing ideas.",
        "project_label": "Project / Brand Name",
        "project_placeholder": "Enter your project name...",
        "industry_label": "Industry",
        "country_label": "Target Country",
        "audience_label": "Target Audience Details",
        "audience_placeholder": "For example: culture-loving youth, startup founders, busy professionals...",
        "seed_label": "Seed Keywords",
        "seed_placeholder": "For example: podcast, stories, audio content, culture, inspiration",
        "url_label": "Website or Page URL",
        "url_placeholder": "For example: https://example.com",
        "button": "Generate Marketing Plan ✨",
        "warning_project": "Please enter the project name to continue.",
        "spinner": "Analyzing inputs and generating content...",
        "success": "Plan prepared for project: ",
        "seo": "🔎 SEO Keywords",
        "primary_keywords": "Primary Keywords",
        "supporting_keywords": "Supporting Keywords",
        "meta_title": "Meta Title",
        "meta_description": "Meta Description",
        "slogans": "✨ Slogans",
        "short_headlines": "📣 Short Headlines",
        "long_headlines": "📢 Long Headlines",
        "descriptions": "📝 Descriptions",
        "ctas": "🚀 CTA Suggestions",
        "ideas": "💡 Content Ideas",
        "url_ok": "URL was checked and page content was used to improve results.",
        "url_bad": "Could not read the URL. Results were generated without page content.",
        "url_invalid": "Invalid URL. It was ignored."
    }


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    if not re.match(r"^https?://", url):
        url = "https://" + url
    return url


def fetch_url_context(url: str) -> dict:
    result = {
        "ok": False,
        "final_url": "",
        "title": "",
        "description": "",
        "content": "",
        "error": ""
    }

    if not url:
        return result

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        meta_desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            meta_desc = meta["content"].strip()

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        visible_text = " ".join(soup.get_text(separator=" ").split())
        visible_text = visible_text[:2500]

        result.update({
            "ok": True,
            "final_url": response.url,
            "title": title,
            "description": meta_desc,
            "content": visible_text
        })
        return result

    except Exception as e:
        result["error"] = str(e)
        return result


top_col1, top_col2 = st.columns([1, 3])
with top_col1:
    lang = st.selectbox("Language / اللغة", ["العربية", "English"])

text = ui_text(lang)

st.title(text["page_title"])
st.write(text["subtitle"])

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        p_name = st.text_input(
            text["project_label"],
            placeholder=text["project_placeholder"]
        )

        industry_options_ar = [
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

        industry_options_en = [
            "Podcast",
            "Technology / SaaS",
            "Real Estate",
            "Food / Cooking",
            "Education",
            "E-commerce",
            "Health / Wellness",
            "Beauty",
            "Sports",
            "Other"
        ]

        industry = st.selectbox(
            text["industry_label"],
            industry_options_ar if lang == "العربية" else industry_options_en
        )

    with col2:
        target_country = st.selectbox(
            text["country_label"],
            ["Egypt", "Saudi Arabia", "UAE", "Sudan", "Global"]
        )

    audience = st.text_area(
        text["audience_label"],
        placeholder=text["audience_placeholder"]
    )

    seed_keywords = st.text_area(
        text["seed_label"],
        placeholder=text["seed_placeholder"]
    )

    website_url = st.text_input(
        text["url_label"],
        placeholder=text["url_placeholder"]
    )

    generate = st.button(text["button"])


if generate:
    if not p_name:
        st.warning(text["warning_project"])
    else:
        tone_instruction = get_country_tone(target_country, lang)

        cleaned_url = normalize_url(website_url)
        url_context = {
            "ok": False,
            "title": "",
            "description": "",
            "content": "",
            "final_url": "",
            "error": ""
        }

        if website_url.strip():
            if cleaned_url.startswith("http://") or cleaned_url.startswith("https://"):
                url_context = fetch_url_context(cleaned_url)
                if url_context["ok"]:
                    st.success(text["url_ok"])
                else:
                    st.warning(text["url_bad"])
            else:
                st.warning(text["url_invalid"])

        url_instruction = ""
        if url_context["ok"]:
            url_instruction = f"""
Website URL checked successfully.
Final URL: {url_context["final_url"]}
Page Title: {url_context["title"]}
Meta Description: {url_context["description"]}
Visible Page Content:
{url_context["content"]}
Use this page context strongly to improve the accuracy of the output.
"""

        prompt = f"""
Act as a Senior SEO & Content Strategist and high-conversion copywriter.

Project Name: {p_name}
Industry: {industry}
Target Country: {target_country}
Language: {lang}
Target Audience: {audience}
Seed Keywords: {seed_keywords}

{url_instruction}

Important writing instruction:
{tone_instruction}

Requirements:
- Make the output feel relevant to the target country.
- If the selected language is Arabic, adapt the wording style to the selected country.
- The entire output must be in the selected language.
- Use the seed keywords naturally.
- If website context is available, use it to improve relevance and accuracy.
- Make the meta title clickable, natural, and SEO-friendly.
- Make the meta description concise and compelling.
- Separate primary keywords from supporting keywords clearly.
- Make short headlines suitable for ads.
- Make long headlines more descriptive and conversion-focused.
- Keep the output marketing-focused, realistic, and usable.
- Avoid generic filler.
- Return ONLY valid JSON.

Return this exact JSON structure:
{{
  "primary_keywords": ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"],
  "supporting_keywords": ["support 1", "support 2", "support 3", "support 4", "support 5"],
  "meta_title": "meta title here",
  "meta_description": "meta description here",
  "slogans": ["slogan 1", "slogan 2", "slogan 3"],
  "short_headlines": ["short 1", "short 2", "short 3", "short 4", "short 5"],
  "long_headlines": ["long 1", "long 2", "long 3", "long 4", "long 5"],
  "descriptions": ["description 1", "description 2", "description 3"],
  "ctas": ["cta 1", "cta 2", "cta 3", "cta 4"],
  "content_ideas": ["idea 1", "idea 2", "idea 3", "idea 4", "idea 5"]
}}
"""

        with st.spinner(text["spinner"]):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

                raw_text = response.text
                res = extract_json(raw_text)

                st.success(f'{text["success"]}{p_name}')

                col_a, col_b = st.columns(2)

                with col_a:
                    st.subheader(text["seo"])

                    st.markdown(f"**{text['primary_keywords']}**")
                    for k in res["primary_keywords"]:
                        st.markdown(
                            f'<div class="small-card">{k}</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown(f"**{text['supporting_keywords']}**")
                    for k in res["supporting_keywords"]:
                        st.markdown(
                            f'<div class="small-card">{k}</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown(f"**{text['meta_title']}**")
                    st.markdown(
                        f'<div class="info-card">{res["meta_title"]}</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(f"**{text['meta_description']}**")
                    st.markdown(
                        f'<div class="info-card">{res["meta_description"]}</div>',
                        unsafe_allow_html=True
                    )

                    st.subheader(text["slogans"])
                    for s in res["slogans"]:
                        st.markdown(
                            f'<div class="info-card">{s}</div>',
                            unsafe_allow_html=True
                        )

                    st.subheader(text["ctas"])
                    for c in res["ctas"]:
                        st.markdown(
                            f'<div class="small-card">{c}</div>',
                            unsafe_allow_html=True
                        )

                with col_b:
                    st.subheader(text["short_headlines"])
                    for h in res["short_headlines"]:
                        st.markdown(
                            f'<div class="info-card">{h}</div>',
                            unsafe_allow_html=True
                        )

                    st.subheader(text["long_headlines"])
                    for h in res["long_headlines"]:
                        st.markdown(
                            f'<div class="info-card">{h}</div>',
                            unsafe_allow_html=True
                        )

                st.subheader(text["descriptions"])
                for d in res["descriptions"]:
                    st.info(d)

                st.subheader(text["ideas"])
                for idea in res["content_ideas"]:
                    st.markdown(
                        f'<div class="small-card">{idea}</div>',
                        unsafe_allow_html=True
                    )

            except Exception as e:
                st.error(f"حدث خطأ: {e}" if lang == "العربية" else f"Error: {e}")

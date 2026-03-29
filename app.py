import json
import re
from collections import Counter

import requests
import streamlit as st
from bs4 import BeautifulSoup
from google import genai

st.set_page_config(layout="wide", page_title="Professional Content Builder")

st.markdown(
    """
<style>
/* ===== App background ===== */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%) !important;
    color: #ffffff !important;
}

.main, .block-container, section.main {
    background: transparent !important;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ===== Typography ===== */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

p, span, div {
    color: #e5e7eb;
}

/* ===== Labels ===== */
label, .stTextInput label, .stSelectbox label, .stTextArea label {
    color: #f8fafc !important;
    font-weight: 700 !important;
}

/* ===== Inputs ===== */
.stTextInput input,
.stTextArea textarea {
    background: #ffffff !important;
    color: #0f172a !important;
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    font-weight: 600 !important;
}

/* ===== Select main closed box ===== */
.stSelectbox div[data-baseweb="select"] > div,
.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] input,
.stSelectbox div[data-baseweb="select"] svg {
    background: #ffffff !important;
    color: #0f172a !important;
    fill: #0f172a !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}

/* ===== Dropdown menu options ===== */
[data-baseweb="menu"],
[data-baseweb="popover"] {
    background: #ffffff !important;
}

[data-baseweb="menu"] *,
[data-baseweb="popover"] *,
li[role="option"],
div[role="listbox"] * {
    color: #0f172a !important;
    background: #ffffff !important;
    font-weight: 600 !important;
}

/* Hover/selected option */
li[role="option"]:hover,
li[aria-selected="true"] {
    background: #dbeafe !important;
    color: #0f172a !important;
}

/* Placeholder */
input::placeholder,
textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* ===== Buttons ===== */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    padding: 13px 16px !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 24px rgba(37, 99, 235, 0.28) !important;
}

.stDownloadButton > button {
    width: 100%;
    background: #1d4ed8 !important;
    color: white !important;
    border: 1px solid #2563eb !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-weight: 700 !important;
}

/* ===== Cards ===== */
.metric-card {
    background: #0b1730 !important;
    border: 1px solid #334155 !important;
    border-radius: 16px !important;
    padding: 16px !important;
    min-height: 88px !important;
    margin-bottom: 10px !important;
}

.metric-label {
    color: #93c5fd !important;
    font-size: 0.9rem !important;
    margin-bottom: 6px !important;
    font-weight: 600 !important;
}

.metric-value {
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 1.08rem !important;
    word-break: break-word !important;
}

.pill {
    display: inline-block;
    padding: 8px 12px;
    border-radius: 999px;
    background: #1d4ed8;
    border: 1px solid #60a5fa;
    margin: 4px 6px 4px 0;
    color: white !important;
    font-size: 0.92rem;
}

/* ===== Tabs ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background: #1e293b !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    color: white !important;
    border: 1px solid #334155 !important;
}

.stTabs [aria-selected="true"] {
    background: #2563eb !important;
    color: white !important;
}

/* ===== Expander ===== */
[data-testid="stExpander"] details {
    background: #0f172a !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

/* ===== Alerts ===== */
.stAlert {
    border-radius: 12px !important;
}

/* ===== Code blocks ===== */
pre, code, [data-testid="stCodeBlock"] {
    border-radius: 12px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

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
            "language_label": "اللغة",
            "project_label": "اسم المشروع / العلامة التجارية",
            "project_placeholder": "أدخلي اسم المشروع هنا...",
            "country_label": "الدولة المستهدفة",
            "industry_label": "مجال العمل",
            "audience_label": "تفاصيل الجمهور المستهدف",
            "audience_placeholder": "مثلاً: الشباب المهتمين بالثقافة، أو أصحاب الشركات الناشئة...",
            "url_label": "رابط الموقع أو الصفحة",
            "url_placeholder": "مثلاً: https://example.com",
            "seed_label": "كلمات إضافية اختيارية",
            "seed_placeholder": "اختياري: كلمات إضافية تريدين دعم النتائج بها",
            "button": "توليد الخطة التسويقية ✨",
            "warning_project": "الرجاء إدخال اسم المشروع للمتابعة.",
            "spinner": "جاري تحليل البيانات وتوليد المحتوى...",
            "success": "تم تجهيز الخطة لمشروع: ",
            "url_ok": "تم التحقق من الرابط واستخدام محتواه لتحسين النتائج.",
            "url_bad": "تعذر قراءة الرابط. سيتم التوليد بدون محتوى الصفحة.",
            "url_invalid": "الرابط غير صالح. سيتم تجاهله.",
            "url_insights": "🔍 تحليل الرابط",
            "page_title_label": "عنوان الصفحة",
            "page_desc_label": "وصف الصفحة",
            "extracted_keywords": "الكلمات المستخرجة من الرابط",
            "download": "تحميل الخطة",
            "download_file": "marketing_plan.txt",
            "seo_tab": "SEO",
            "ads_tab": "Ads",
            "ideas_tab": "Ideas",
            "project_metric": "المشروع",
            "country_metric": "الدولة",
            "industry_metric": "المجال",
            "primary_keywords": "الكلمات المفتاحية الأساسية",
            "supporting_keywords": "الكلمات المفتاحية الداعمة",
            "meta_title": "عنوان الميتا",
            "meta_description": "وصف الميتا",
            "slogans": "✨ الشعارات",
            "short_headlines": "📣 العناوين القصيرة",
            "long_headlines": "📢 العناوين الطويلة",
            "descriptions": "📝 الوصف التسويقي",
            "ctas": "🚀 الاقتراحات",
            "ideas": "💡 أفكار المحتوى",
        }
    return {
        "page_title": "🚀 Smart Content Builder",
        "subtitle": "A professional tool to generate SEO plans, slogans, headlines, descriptions, and marketing ideas.",
        "language_label": "Language",
        "project_label": "Project / Brand Name",
        "project_placeholder": "Enter your project name...",
        "country_label": "Target Country",
        "industry_label": "Industry",
        "audience_label": "Target Audience Details",
        "audience_placeholder": "For example: culture-loving youth, startup founders, busy professionals...",
        "url_label": "Website or Page URL",
        "url_placeholder": "For example: https://example.com",
        "seed_label": "Optional Extra Keywords",
        "seed_placeholder": "Optional: extra terms you want to support the results with",
        "button": "Generate Marketing Plan ✨",
        "warning_project": "Please enter the project name to continue.",
        "spinner": "Analyzing inputs and generating content...",
        "success": "Plan prepared for project: ",
        "url_ok": "URL was checked and page content was used to improve results.",
        "url_bad": "Could not read the URL. Results were generated without page content.",
        "url_invalid": "Invalid URL. It was ignored.",
        "url_insights": "🔍 URL Analysis",
        "page_title_label": "Page Title",
        "page_desc_label": "Page Description",
        "extracted_keywords": "Keywords Extracted From URL",
        "download": "Download Plan",
        "download_file": "marketing_plan.txt",
        "seo_tab": "SEO",
        "ads_tab": "Ads",
        "ideas_tab": "Ideas",
        "project_metric": "Project",
        "country_metric": "Country",
        "industry_metric": "Industry",
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
        "headings": [],
        "error": "",
    }

    if not url:
        return result

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True,
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

        headings = []
        for tag_name in ["h1", "h2", "h3"]:
            for tag in soup.find_all(tag_name):
                txt = " ".join(tag.get_text(separator=" ").split()).strip()
                if txt:
                    headings.append(txt)

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        visible_text = " ".join(soup.get_text(separator=" ").split())
        visible_text = visible_text[:3000]

        result.update(
            {
                "ok": True,
                "final_url": response.url,
                "title": title,
                "description": meta_desc,
                "content": visible_text,
                "headings": headings[:10],
            }
        )
        return result

    except Exception as e:
        result["error"] = str(e)
        return result


AR_STOPWORDS = {
    "في", "من", "على", "إلى", "عن", "مع", "هذا", "هذه", "ذلك", "تلك", "هو", "هي",
    "كما", "تم", "او", "أو", "و", "يا", "ما", "لا", "لم", "لن", "كل", "أي", "أن",
    "إن", "الى", "the", "and",
}

EN_STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "your", "you", "into",
    "are", "our", "was", "were", "will", "have", "has", "had", "about", "more",
    "than", "their", "they", "them", "www", "com", "https", "http",
}


def tokenize_text(text: str, lang: str) -> list[str]:
    tokens = re.findall(r"[A-Za-z\u0600-\u06FF]{2,}", text.lower())
    stopwords = AR_STOPWORDS if lang == "العربية" else EN_STOPWORDS
    return [t for t in tokens if t not in stopwords and len(t) > 2]


def extract_keywords_from_url_context(url_context: dict, lang: str) -> list[str]:
    if not url_context["ok"]:
        return []

    weighted_text_parts = []

    if url_context["title"]:
        weighted_text_parts.extend([url_context["title"]] * 4)

    if url_context["description"]:
        weighted_text_parts.extend([url_context["description"]] * 3)

    for h in url_context.get("headings", []):
        weighted_text_parts.extend([h] * 3)

    if url_context["content"]:
        weighted_text_parts.append(url_context["content"])

    combined = " ".join(weighted_text_parts)
    tokens = tokenize_text(combined, lang)
    if not tokens:
        return []

    counts = Counter(tokens)
    bigrams = Counter()

    for part in weighted_text_parts:
        part_tokens = tokenize_text(part, lang)
        for i in range(len(part_tokens) - 1):
            bg = f"{part_tokens[i]} {part_tokens[i + 1]}"
            if len(bg) > 5:
                bigrams[bg] += 1

    candidates = []
    for word, count in counts.most_common(40):
        candidates.append((word, count))
    for phrase, count in bigrams.most_common(40):
        candidates.append((phrase, count + 2))

    ranked = sorted(candidates, key=lambda x: x[1], reverse=True)

    final_keywords = []
    seen = set()
    for kw, _ in ranked:
        key = kw.lower()
        if key not in seen:
            seen.add(key)
            final_keywords.append(kw)
        if len(final_keywords) >= 20:
            break

    return final_keywords


def split_extra_keywords(text: str) -> list[str]:
    return [k.strip() for k in text.split(",") if k.strip()]


def list_to_text(items):
    return "\n".join([f"- {item}" for item in items])


def build_download_text(res: dict, text: dict, project_name: str) -> str:
    parts = [
        f"{text['success']}{project_name}",
        "",
        text["primary_keywords"],
        list_to_text(res["primary_keywords"]),
        "",
        text["supporting_keywords"],
        list_to_text(res["supporting_keywords"]),
        "",
        text["meta_title"],
        res["meta_title"],
        "",
        text["meta_description"],
        res["meta_description"],
        "",
        text["slogans"],
        list_to_text(res["slogans"]),
        "",
        text["short_headlines"],
        list_to_text(res["short_headlines"]),
        "",
        text["long_headlines"],
        list_to_text(res["long_headlines"]),
        "",
        text["descriptions"],
        list_to_text(res["descriptions"]),
        "",
        text["ctas"],
        list_to_text(res["ctas"]),
        "",
        text["ideas"],
        list_to_text(res["content_ideas"]),
    ]
    return "\n".join(parts)


if "lang" not in st.session_state:
    st.session_state.lang = "العربية"

lang = st.session_state.lang
text = ui_text(lang)

st.title(text["page_title"])
st.write(text["subtitle"])

with st.container():
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        lang = st.selectbox(
            "Language / اللغة",
            ["العربية", "English"],
            key="lang",
        )
        text = ui_text(lang)

        p_name = st.text_input(
            text["project_label"],
            placeholder=text["project_placeholder"],
        )

        target_country = st.selectbox(
            text["country_label"],
            ["Egypt", "Saudi Arabia", "UAE", "Sudan", "Global"],
        )

        industry_options_ar = [
            "بودكاست", "تقنية/SaaS", "عقارات", "طبخ/أغذية", "تعليم",
            "تجارة إلكترونية", "صحة/عافية", "جمال", "رياضة", "أخرى",
        ]
        industry_options_en = [
            "Podcast", "Technology / SaaS", "Real Estate", "Food / Cooking",
            "Education", "E-commerce", "Health / Wellness", "Beauty", "Sports", "Other",
        ]

        industry = st.selectbox(
            text["industry_label"],
            industry_options_ar if lang == "العربية" else industry_options_en,
        )

        audience = st.text_area(
            text["audience_label"],
            placeholder=text["audience_placeholder"],
        )

        website_url = st.text_input(
            text["url_label"],
            placeholder=text["url_placeholder"],
        )

        extra_keywords = st.text_area(
            text["seed_label"],
            placeholder=text["seed_placeholder"],
        )

        generate = st.button(text["button"])

    with right:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{text["project_metric"]}</div><div class="metric-value">{p_name if p_name else "—"}</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{text["country_metric"]}</div><div class="metric-value">{target_country if target_country else "—"}</div></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{text["industry_metric"]}</div><div class="metric-value">{industry if industry else "—"}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("### URL & AI Preview")
        st.write("Paste a page URL and the app will try to extract title, description, headings, and on-page keyword signals automatically.")


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
            "headings": [],
            "final_url": "",
            "error": "",
        }

        extracted_keywords = []
        extra_keywords_list = split_extra_keywords(extra_keywords)

        if website_url.strip():
            if cleaned_url.startswith("http://") or cleaned_url.startswith("https://"):
                url_context = fetch_url_context(cleaned_url)
                if url_context["ok"]:
                    st.success(text["url_ok"])
                    extracted_keywords = extract_keywords_from_url_context(url_context, lang)
                else:
                    st.warning(text["url_bad"])
            else:
                st.warning(text["url_invalid"])

        merged_keywords = []
        seen_keywords = set()
        for kw in extracted_keywords + extra_keywords_list:
            key = kw.lower()
            if kw and key not in seen_keywords:
                merged_keywords.append(kw)
                seen_keywords.add(key)

        url_instruction = ""
        if url_context["ok"]:
            url_instruction = f"""
Website URL checked successfully.
Final URL: {url_context["final_url"]}
Page Title: {url_context["title"]}
Meta Description: {url_context["description"]}
Headings: {", ".join(url_context["headings"])}
Visible Page Content:
{url_context["content"]}

Automatically extracted keyword candidates from the page:
{", ".join(extracted_keywords)}

Use this page context strongly to improve the accuracy of the output.
"""

        prompt = f"""
Act as a Senior SEO & Content Strategist and high-conversion copywriter.

Project Name: {p_name}
Industry: {industry}
Target Country: {target_country}
Language: {lang}
Target Audience: {audience}

Keyword guidance:
Use these keyword candidates as primary context when relevant:
{", ".join(merged_keywords)}

{url_instruction}

Important writing instruction:
{tone_instruction}

Requirements:
- Make the output feel relevant to the target country.
- If the selected language is Arabic, adapt the wording style to the selected country.
- The entire output must be in the selected language.
- If website context is available, use it to improve relevance and accuracy.
- Use the automatically extracted keywords from the URL when helpful.
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
  "primary_keywords": ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5", "keyword 6", "keyword 7", "keyword 8", "keyword 9", "keyword 10"],
  "supporting_keywords": ["support 1", "support 2", "support 3", "support 4", "support 5", "support 6", "support 7", "support 8", "support 9", "support 10"],
  "meta_title": "meta title here",
  "meta_description": "meta description here",
  "slogans": ["slogan 1", "slogan 2", "slogan 3", "slogan 4", "slogan 5", "slogan 6", "slogan 7", "slogan 8", "slogan 9", "slogan 10"],
  "short_headlines": ["short 1", "short 2", "short 3", "short 4", "short 5", "short 6", "short 7", "short 8", "short 9", "short 10"],
  "long_headlines": ["long 1", "long 2", "long 3", "long 4", "long 5", "long 6", "long 7", "long 8", "long 9", "long 10"],
  "descriptions": ["description 1", "description 2", "description 3", "description 4", "description 5", "description 6", "description 7", "description 8", "description 9", "description 10"],
  "ctas": ["cta 1", "cta 2", "cta 3", "cta 4", "cta 5", "cta 6", "cta 7", "cta 8", "cta 9", "cta 10"],
  "content_ideas": ["idea 1", "idea 2", "idea 3", "idea 4", "idea 5", "idea 6", "idea 7", "idea 8", "idea 9", "idea 10"]
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

                if url_context["ok"]:
                    with st.expander(text["url_insights"], expanded=False):
                        if url_context["title"]:
                            st.markdown(f"**{text['page_title_label']}:** {url_context['title']}")
                        if url_context["description"]:
                            st.markdown(f"**{text['page_desc_label']}:** {url_context['description']}")
                        if extracted_keywords:
                            st.markdown(f"**{text['extracted_keywords']}:**")
                            st.markdown(
                                "".join([f'<span class="pill">{kw}</span>' for kw in extracted_keywords]),
                                unsafe_allow_html=True,
                            )

                plan_text = build_download_text(res, text, p_name)
                st.download_button(
                    label=text["download"],
                    data=plan_text,
                    file_name=text["download_file"],
                    mime="text/plain",
                )

                tab1, tab2, tab3 = st.tabs([
                    text["seo_tab"],
                    text["ads_tab"],
                    text["ideas_tab"],
                ])

                with tab1:
                    st.markdown(f"**{text['primary_keywords']}**")
                    st.code("\n".join(res["primary_keywords"]), language=None)

                    st.markdown(f"**{text['supporting_keywords']}**")
                    st.code("\n".join(res["supporting_keywords"]), language=None)

                    st.markdown(f"**{text['meta_title']}**")
                    st.code(res["meta_title"], language=None)

                    st.markdown(f"**{text['meta_description']}**")
                    st.code(res["meta_description"], language=None)

                with tab2:
                    col_a, col_b = st.columns(2)

                    with col_a:
                        st.subheader(text["slogans"])
                        st.code("\n".join(res["slogans"]), language=None)

                        st.subheader(text["ctas"])
                        st.code("\n".join(res["ctas"]), language=None)

                    with col_b:
                        st.subheader(text["short_headlines"])
                        st.code("\n".join(res["short_headlines"]), language=None)

                        st.subheader(text["long_headlines"])
                        st.code("\n".join(res["long_headlines"]), language=None)

                    st.subheader(text["descriptions"])
                    st.code("\n".join(res["descriptions"]), language=None)

                with tab3:
                    st.subheader(text["ideas"])
                    st.code("\n".join(res["content_ideas"]), language=None)

            except Exception as e:
                st.error(f"حدث خطأ: {e}" if lang == "العربية" else f"Error: {e}")

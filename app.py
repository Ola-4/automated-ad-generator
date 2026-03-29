import json
import re
from collections import Counter

import requests
import streamlit as st
from bs4 import BeautifulSoup
from google import genai

st.set_page_config(layout="wide", page_title="Professional Content Builder")

st.markdown("""
<style>
/* ===== Force dark background everywhere ===== */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {
    background: linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%) !important;
    color: #ffffff !important;
}

[data-testid="stAppViewContainer"] > .main,
section.main,
.block-container {
    background: transparent !important;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ===== Headings ===== */
h1 {
    color: #ffffff !important;
    font-weight: 800 !important;
    margin-bottom: 0.35rem !important;
    letter-spacing: -0.4px;
}

h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

p {
    color: #e5e7eb !important;
    font-size: 1rem;
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
    font-weight: 500 !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #0f172a !important;
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    font-weight: 500 !important;
}

/* Dropdown menu text */
[data-baseweb="menu"] *,
[data-baseweb="popover"] * {
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

/* ===== Metric cards ===== */
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

/* ===== Panel card ===== */
.panel-card {
    background: #0f172a !important;
    border: 1px solid #334155 !important;
    border-radius: 18px !important;
    padding: 18px !important;
}

/* ===== Pills ===== */
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

/* ===== Code blocks ===== */
pre, code, [data-testid="stCodeBlock"] {
    border-radius: 12px !important;
}

/* ===== Alerts ===== */
.stAlert {
    border-radius: 12px !important;
}

/* ===== Expander ===== */
[data-testid="stExpander"] details {
    background: #0f172a !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
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
            "seed_label": "كلمات إضافية اختيارية",
            "seed_placeholder": "اختياري: كلمات إضافية تريدين دعم النتائج بها",
            "url_label": "رابط الموقع أو الصفحة",
            "url_placeholder": "مثلاً: https://example.com",
            "button": "توليد الخطة التسويقية ✨",
            "warning_project": "الرجاء إدخال اسم المشروع للمتابعة.",
            "spinner": "جاري تحليل البيانات وتوليد المحتوى...",
            "success": "تم تجهيز الخطة لمشروع: ",
            "seo": "🔎 SEO",
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
            "url_ok": "تم التحقق من الرابط واستخدام محتواه لتحسين النتائج.",
            "url_bad": "تعذر قراءة الرابط. سيتم التوليد بدون محتوى الصفحة.",
            "url_invalid": "الرابط غير صالح. سيتم تجاهله.",
            "download": "تحميل الخطة",
            "download_file": "marketing_plan.txt",
            "url_insights": "🔍 تحليل الرابط",
            "page_title_label": "عنوان الصفحة",
            "page_desc_label": "وصف الصفحة",
            "extracted_keywords": "الكلمات المستخرجة من الرابط",
            "seo_tab": "SEO",
            "ads_tab": "Ads",
            "ideas_tab": "Ideas",
            "project_metric": "المشروع",
            "country_metric": "الدولة",
            "industry_metric": "المجال"
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
        "seed_label": "Optional Extra Keywords",
        "seed_placeholder": "Optional: extra terms you want to support the results with",
        "url_label": "Website or Page URL",
        "url_placeholder": "For example: https://example.com",
        "button": "Generate Marketing Plan ✨",
        "warning_project": "Please enter the project name to continue.",
        "spinner": "Analyzing inputs and generating content...",
        "success": "Plan prepared for project: ",
        "seo": "🔎 SEO",
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
        "url_invalid": "Invalid URL. It was ignored.",
        "download": "Download Plan",
        "download_file": "marketing_plan.txt",
        "url_insights": "🔍 URL Analysis",
        "page_title_label": "Page Title",
        "page_desc_label": "Page Description",
        "extracted_keywords": "Keywords Extracted From URL",
        "seo_tab": "SEO",
        "ads_tab": "Ads",
        "ideas_tab": "Ideas",
        "project_metric": "Project",
        "country_metric": "Country",
        "industry_metric": "Industry"
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

        result.update({
            "ok": True,
            "final_url": response.url,
            "title": title,
            "description": meta_desc,
            "content": visible_text,
            "headings": headings[:10]
        })
        return result

    except Exception as e:
        result["error"] = str(e)
        return result


AR_STOPWORDS = {
    "في", "من", "على", "إلى", "عن", "مع", "هذا", "هذه", "ذلك", "تلك", "هو", "هي",
    "كما", "تم", "او", "أو", "و", "يا", "ما", "لا", "لم", "لن", "كل", "أي", "أن",
    "إن", "الى", "the", "and"
}

EN_STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "your", "you", "into",
    "are", "our", "was", "were", "will", "have", "has", "had", "about", "more",
    "than", "into", "their", "they", "them", "www", "com", "https", "http"
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
            bg = f"{part_tokens[i]} {part_tokens[i+1]}"
            if len(bg) > 5:
                bigrams[bg] += 1

    candidates = []

    for word, count in counts.most_common(20):
        candidates.append((word, count))

    for phrase, count in bigrams.most_common(20):
        candidates.append((phrase, count + 2))

    ranked = sorted(candidates, key=lambda x: x[1], reverse=True)

    final_keywords = []
    seen = set()
    for kw, _ in ranked:
        if kw not in seen:
            seen.add(kw)
            final_keywords.append(kw)
        if len(final_keywords) >= 12:
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
            key="lang"
        )
        text = ui_text(lang)

        p_name = st.text_input(
            text["project_label"],
            placeholder=text["project_placeholder"]
        )

        target_country = st.selectbox(
            text["country_label"],
            ["Egypt", "Saudi Arabia", "UAE", "Sudan", "Global"]
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

        audience = st.text_area(
            text["audience_label"],
            placeholder=text["audience_placeholder"]
        )

        website_url = st.text_input(
            text["url_label"],
            placeholder=text["url_placeholder"]
        )

        extra_keywords = st.text_area(
            text["seed_label"],
            placeholder=text["seed_placeholder"]
        )

        generate = st.button(text["button"])

    with right:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{text["project_metric"]}</div><div class="metric-value">{p_name if p_name else "—"}</div></div>',
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{text["country_metric"]}</div><div class="metric-value">{target_country if target_country else "—"}</div></div>',
                unsafe_allow_html=True
            )
        with c3:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{text["industry_metric"]}</div><div class="metric-value">{industry if industry else "—"}</div></div>',
                unsafe_allow_html=True
            )

        st.markdown

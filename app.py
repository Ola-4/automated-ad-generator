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

h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

p, span, div {
    color: #e5e7eb !important;
}

label, .stTextInput label, .stSelectbox label, .stTextArea label {
    color: #f8fafc !important;
    font-weight: 700 !important;
}

.stTextInput input,
.stTextArea textarea {
    background: #ffffff !important;
    color: #0f172a !important;
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    font-weight: 600 !important;
}

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

li[role="option"]:hover,
li[aria-selected="true"] {
    background: #dbeafe !important;
    color: #0f172a !important;
}

input::placeholder,
textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

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
    background: #1d4ed8 !important;
    border: 1px solid #60a5fa !important;
    margin: 4px 6px 4px 0;
    color: white !important;
    font-size: 0.92rem;
}

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

[data-testid="stExpander"] details {
    background: #0f172a !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

.stAlert {
    border-radius: 12px !important;
}

[data-testid="stCodeBlock"] {
    background: #0b1730 !important;
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
}

[data-testid="stCodeBlock"] pre,
[data-testid="stCodeBlock"] code,
.stCode, .stCodeBlock, pre, code {
    background: #0b1730 !important;
    color: #f8fafc !important;
    border-radius: 14px !important;
}

[data-testid="stCodeBlock"] button {
    color: white !important;
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


def init_state() -> None:
    defaults = {
        "lang": "العربية",
        "project_name": "",
        "target_country": "Egypt",
        "industry": "بودكاست",
        "audience": "",
        "website_url": "",
        "extra_keywords": "",
        "generated": False,
        "result": None,
        "url_context": None,
        "extracted_keywords": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_form() -> None:
    st.session_state.lang = "العربية"
    st.session_state.project_name = ""
    st.session_state.target_country = "Egypt"
    st.session_state.industry = "بودكاست"
    st.session_state.audience = ""
    st.session_state.website_url = ""
    st.session_state.extra_keywords = ""
    st.session_state.generated = False
    st.session_state.result = None
    st.session_state.url_context = None
    st.session_state.extracted_keywords = []


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
            "generate_button": "توليد الخطة التسويقية ✨",
            "reset_button": "إعادة ضبط",
            "warning_project": "الرجاء إدخال اسم المشروع للمتابعة.",
            "spinner": "جاري تحليل البيانات وتوليد المحتوى...",
            "success": "تم تجهيز الخطة لمشروع: ",
            "url_ok": "تم التحقق من الرابط واستخدام محتواه لتحسين النتائج.",
            "url_bad": "تعذر قراءة الرابط. سيتم التوليد بدون محتوى الصفحة.",
            "url_invalid": "الرابط غير صالح. سيتم تجاهله.",
            "url_insights": "🔍 تحليل الرابط",
            "page_title_label": "عنوان الصفحة",
            "page_desc_label": "وصف الصفحة",
            "meta_keywords_label": "Meta Keywords",
            "headings_label": "العناوين",
            "link_texts_label": "نصوص الروابط",
            "list_items_label": "القوائم",
            "alt_texts_label": "Alt Text",
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
            "preview_text": "ألصقي رابط صفحة وسيحاول التطبيق استخراج العناوين، التصنيفات، نصوص الروابط، وأهم إشارات الكلمات المفتاحية تلقائيًا.",
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
        "generate_button": "Generate Marketing Plan ✨",
        "reset_button": "Reset",
        "warning_project": "Please enter the project name to continue.",
        "spinner": "Analyzing inputs and generating content...",
        "success": "Plan prepared for project: ",
        "url_ok": "URL was checked and page content was used to improve results.",
        "url_bad": "Could not read the URL. Results were generated without page content.",
        "url_invalid": "Invalid URL. It was ignored.",
        "url_insights": "🔍 URL Analysis",
        "page_title_label": "Page Title",
        "page_desc_label": "Page Description",
        "meta_keywords_label": "Meta Keywords",
        "headings_label": "Headings",
        "link_texts_label": "Link Texts",
        "list_items_label": "List Items",
        "alt_texts_label": "Image Alt Texts",
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
        "preview_text": "Paste a page URL and the app will try to extract titles, categories, link texts, and on-page keyword signals automatically.",
    }


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    if not re.match(r"^https?://", url):
        url = "https://" + url
    return url


def clean_text(value: str) -> str:
    return " ".join(value.split()).strip()


def unique_keep_order(items):
    seen = set()
    result = []
    for item in items:
        key = item.lower().strip()
        if item and key not in seen:
            seen.add(key)
            result.append(item.strip())
    return result


def fetch_url_context(url: str) -> dict:
    result = {
        "ok": False,
        "final_url": "",
        "title": "",
        "description": "",
        "meta_keywords": [],
        "content": "",
        "headings": [],
        "link_texts": [],
        "list_items": [],
        "alt_texts": [],
        "content_blocks": [],
        "error": "",
    }

    if not url:
        return result

    try:
        response = requests.get(
            url,
            timeout=12,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = ""
        if soup.title and soup.title.string:
            title = clean_text(soup.title.string)

        meta_desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            meta_desc = clean_text(meta["content"])

        meta_keywords = []
        meta_kw = soup.find("meta", attrs={"name": "keywords"})
        if meta_kw and meta_kw.get("content"):
            meta_keywords = [clean_text(x) for x in meta_kw["content"].split(",") if clean_text(x)]

        headings = []
        for tag_name in ["h1", "h2", "h3"]:
            for tag in soup.find_all(tag_name):
                txt = clean_text(tag.get_text(separator=" "))
                if txt:
                    headings.append(txt)

        link_texts = []
        for a in soup.find_all("a"):
            txt = clean_text(a.get_text(separator=" "))
            if txt and len(txt) <= 120:
                link_texts.append(txt)

        list_items = []
        for li in soup.find_all("li"):
            txt = clean_text(li.get_text(separator=" "))
            if txt and 2 <= len(txt.split()) <= 20:
                list_items.append(txt)

        alt_texts = []
        for img in soup.find_all("img"):
            alt = clean_text(img.get("alt", ""))
            if alt:
                alt_texts.append(alt)

        content_blocks = []
        selectors = [
            "article", "section", "main", ".card", ".post", ".book", ".title",
            ".category", ".content", ".entry", ".product", ".item"
        ]
        for selector in selectors:
            for tag in soup.select(selector):
                txt = clean_text(tag.get_text(separator=" "))
                if txt and len(txt) > 20:
                    content_blocks.append(txt)

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        visible_text = clean_text(soup.get_text(separator=" "))
        visible_text = visible_text[:5000]

        result.update(
            {
                "ok": True,
                "final_url": response.url,
                "title": title,
                "description": meta_desc,
                "meta_keywords": unique_keep_order(meta_keywords)[:50],
                "content": visible_text,
                "headings": unique_keep_order(headings)[:40],
                "link_texts": unique_keep_order(link_texts)[:80],
                "list_items": unique_keep_order(list_items)[:80],
                "alt_texts": unique_keep_order(alt_texts)[:40],
                "content_blocks": unique_keep_order(content_blocks)[:40],
            }
        )
        return result

    except Exception as e:
        result["error"] = str(e)
        return result


AR_STOPWORDS = {
    "في", "من", "على", "إلى", "عن", "مع", "هذا", "هذه", "ذلك", "تلك", "هو", "هي",
    "كما", "تم", "او", "أو", "و", "يا", "ما", "لا", "لم", "لن", "كل", "أي", "أن",
    "إن", "الى", "the", "and", "فيه", "لها", "له", "فيها", "عند", "بعد",
}

EN_STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "your", "you", "into",
    "are", "our", "was", "were", "will", "have", "has", "had", "about", "more",
    "than", "their", "they", "them", "www", "com", "https", "http", "home",
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
        weighted_text_parts.extend([url_context["title"]] * 6)

    if url_context["description"]:
        weighted_text_parts.extend([url_context["description"]] * 5)

    for kw in url_context.get("meta_keywords", []):
        weighted_text_parts.extend([kw] * 6)

    for h in url_context.get("headings", []):
        weighted_text_parts.extend([h] * 5)

    for x in url_context.get("link_texts", [])[:50]:
        weighted_text_parts.extend([x] * 3)

    for x in url_context.get("list_items", [])[:50]:
        weighted_text_parts.extend([x] * 4)

    for x in url_context.get("alt_texts", [])[:30]:
        weighted_text_parts.extend([x] * 2)

    for x in url_context.get("content_blocks", [])[:30]:
        weighted_text_parts.extend([x] * 3)

    if url_context.get("content"):
        weighted_text_parts.append(url_context["content"])

    combined = " ".join(weighted_text_parts)
    tokens = tokenize_text(combined, lang)
    if not tokens:
        return []

    counts = Counter(tokens)
    bigrams = Counter()
    trigrams = Counter()

    for part in weighted_text_parts:
        part_tokens = tokenize_text(part, lang)

        for i in range(len(part_tokens) - 1):
            bg = f"{part_tokens[i]} {part_tokens[i + 1]}"
            if len(bg) > 5:
                bigrams[bg] += 1

        for i in range(len(part_tokens) - 2):
            tg = f"{part_tokens[i]} {part_tokens[i + 1]} {part_tokens[i + 2]}"
            if len(tg) > 8:
                trigrams[tg] += 1

    candidates = []

    for word, count in counts.most_common(80):
        candidates.append((word, count))

    for phrase, count in bigrams.most_common(80):
        candidates.append((phrase, count + 3))

    for phrase, count in trigrams.most_common(60):
        candidates.append((phrase, count + 5))

    ranked = sorted(candidates, key=lambda x: x[1], reverse=True)

    final_keywords = []
    seen = set()
    for kw, _ in ranked:
        key = kw.lower().strip()
        if key not in seen:
            seen.add(key)
            final_keywords.append(kw)
        if len(final_keywords) >= 40:
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


def generate_plan() -> None:
    lang = st.session_state.lang
    text = ui_text(lang)

    p_name = st.session_state.project_name
    target_country = st.session_state.target_country
    industry = st.session_state.industry
    audience = st.session_state.audience
    website_url = st.session_state.website_url
    extra_keywords = st.session_state.extra_keywords

    if not p_name:
        st.warning(text["warning_project"])
        return

    tone_instruction = get_country_tone(target_country, lang)

    cleaned_url = normalize_url(website_url)
    url_context = {
        "ok": False,
        "title": "",
        "description": "",
        "meta_keywords": [],
        "content": "",
        "headings": [],
        "link_texts": [],
        "list_items": [],
        "alt_texts": [],
        "content_blocks": [],
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
Meta Keywords: {", ".join(url_context["meta_keywords"])}
Headings: {", ".join(url_context["headings"][:30])}
Link Texts: {", ".join(url_context["link_texts"][:40])}
List Items: {", ".join(url_context["list_items"][:40])}
Image Alt Texts: {", ".join(url_context["alt_texts"][:30])}
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
- If website context is available, use it strongly.
- Use categories, titles, item names, and repeated concepts found on the page.
- Make the output realistic and useful for SEO and campaigns.
- Make the meta title clickable, natural, and SEO-friendly.
- Make the meta description concise and compelling.
- Separate primary keywords from supporting keywords clearly.
- Make short headlines suitable for ads.
- Make long headlines more descriptive and conversion-focused.
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
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        raw_text = response.text
        res = extract_json(raw_text)

    st.session_state.generated = True
    st.session_state.result = res
    st.session_state.url_context = url_context
    st.session_state.extracted_keywords = extracted_keywords


init_state()

lang = st.session_state.lang
text = ui_text(lang)

st.title(text["page_title"])
st.write(text["subtitle"])

with st.container():
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.selectbox(
            "Language / اللغة",
            ["العربية", "English"],
            key="lang",
        )
        text = ui_text(st.session_state.lang)

        industry_options_ar = [
            "بودكاست", "تقنية/SaaS", "عقارات", "طبخ/أغذية", "تعليم",
            "تجارة إلكترونية", "صحة/عافية", "جمال", "رياضة", "أخرى",
        ]
        industry_options_en = [
            "Podcast", "Technology / SaaS", "Real Estate", "Food / Cooking",
            "Education", "E-commerce", "Health / Wellness", "Beauty", "Sports", "Other",
        ]

        st.text_input(
            text["project_label"],
            placeholder=text["project_placeholder"],
            key="project_name",
        )

        st.selectbox(
            text["country_label"],
            ["Egypt", "Saudi Arabia", "UAE", "Sudan", "Global"],
            key="target_country",
        )

        current_industry_options = industry_options_ar if st.session_state.lang == "العربية" else industry_options_en
        if st.session_state.industry not in current_industry_options:
            st.session_state.industry = current_industry_options[0]

        st.selectbox(
            text["industry_label"],
            current_industry_options,
            key="industry",
        )

        st.text_area(
            text["audience_label"],
            placeholder=text["audience_placeholder"],
            key="audience",
        )

        st.text_input(
            text["url_label"],
            placeholder=text["url_placeholder"],
            key="website_url",
        )

        st.text_area(
            text["seed_label"],
            placeholder=text["seed_placeholder"],
            key="extra_keywords",
        )

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.button(text["generate_button"], on_click=generate_plan, use_container_width=True)
        with btn_col2:
            st.button(text["reset_button"], on_click=reset_form, use_container_width=True)

    with right:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{text["project_metric"]}</div><div class="metric-value">{st.session_state.project_name if st.session_state.project_name else "—"}</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{text["country_metric"]}</div><div class="metric-value">{st.session_state.target_country if st.session_state.target_country else "—"}</div></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{text["industry_metric"]}</div><div class="metric-value">{st.session_state.industry if st.session_state.industry else "—"}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("### URL & AI Preview")
        st.write(text["preview_text"])


if st.session_state.generated and st.session_state.result:
    res = st.session_state.result
    url_context = st.session_state.url_context or {}
    extracted_keywords = st.session_state.extracted_keywords or []

    st.success(f'{text["success"]}{st.session_state.project_name}')

    if url_context.get("ok"):
        with st.expander(text["url_insights"], expanded=False):
            if url_context.get("title"):
                st.markdown(f"**{text['page_title_label']}:** {url_context['title']}")
            if url_context.get("description"):
                st.markdown(f"**{text['page_desc_label']}:** {url_context['description']}")
            if url_context.get("meta_keywords"):
                st.markdown(f"**{text['meta_keywords_label']}:**")
                st.markdown("".join([f'<span class="pill">{x}</span>' for x in url_context["meta_keywords"][:20]]), unsafe_allow_html=True)
            if url_context.get("headings"):
                st.markdown(f"**{text['headings_label']}:**")
                st.markdown("".join([f'<span class="pill">{x}</span>' for x in url_context["headings"][:20]]), unsafe_allow_html=True)
            if url_context.get("link_texts"):
                st.markdown(f"**{text['link_texts_label']}:**")
                st.markdown("".join([f'<span class="pill">{x}</span>' for x in url_context["link_texts"][:20]]), unsafe_allow_html=True)
            if url_context.get("list_items"):
                st.markdown(f"**{text['list_items_label']}:**")
                st.markdown("".join([f'<span class="pill">{x}</span>' for x in url_context["list_items"][:20]]), unsafe_allow_html=True)
            if url_context.get("alt_texts"):
                st.markdown(f"**{text['alt_texts_label']}:**")
                st.markdown("".join([f'<span class="pill">{x}</span>' for x in url_context["alt_texts"][:20]]), unsafe_allow_html=True)
            if extracted_keywords:
                st.markdown(f"**{text['extracted_keywords']}:**")
                st.markdown("".join([f'<span class="pill">{kw}</span>' for kw in extracted_keywords[:30]]), unsafe_allow_html=True)

    plan_text = build_download_text(res, text, st.session_state.project_name)
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

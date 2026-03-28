import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json

st.set_page_config(layout="wide", page_title="Smart Ads & SEO Builder")

# تنسيق الشاشة الكاملة
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .main .block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
        iframe { width: 100% !important; border: none !important; min-height: 100vh; }
    </style>
    """, unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

def get_ai_content(data):
    # التأكد من أن البيانات قاموس وليست فارغة
    if not data or not isinstance(data, dict) or not data.get('project'):
        return None
    
    prompt = f"""
    Act as a Senior Marketing Expert. 
    Project: {data['project']}, Industry: {data['industry']}, 
    Country: {data['country']}, Language: {data['language']}.
    Target Audience: {data.get('audience', 'General')}.
    
    INSTRUCTION: If Arabic is selected, use the local dialect of {data['country']} for Slogans and Headlines.
    Return ONLY a JSON object with: primaryKeywords, slogans, shortHeadlines, descriptions.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.replace('```json', '').replace('```', '').strip()
    except:
        return None

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# استلام المدخلات
user_input = components.html(html_code, height=2000, scrolling=True)

# التأمين ضد الـ TypeError (السطر المنقذ)
if user_input and isinstance(user_input, dict) and user_input.get('project'):
    with st.spinner("AI is crafting your results..."):
        ai_res = get_ai_content(user_input)
        if ai_res:
            final_html = html_code.replace("/*AI_DATA_PLACEHOLDER*/", f"const ai_output = {ai_res};")
            components.html(final_html, height=2000, scrolling=True)

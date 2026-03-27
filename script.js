function showLoader() {
  document.getElementById("loader").classList.remove("hidden");
}

function hideLoader() {
  document.getElementById("loader").classList.add("hidden");
}

function extractDomain(url) {
  try {
    const u = new URL(url);
    return u.hostname.replace("www.", "");
  } catch {
    return "";
  }
}

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 1800);
}

function updateDirection(language) {
  const body = document.body;
  if (language === "ar") {
    body.setAttribute("dir", "rtl");
    body.setAttribute("lang", "ar");
  } else {
    body.setAttribute("dir", "ltr");
    body.setAttribute("lang", "en");
  }
}

function parseSeedKeywords(seedText) {
  return seedText
    .split(",")
    .map(item => item.trim())
    .filter(Boolean);
}

function uniqueList(items) {
  return [...new Set(items.filter(Boolean))];
}

// --- الدالة الأساسية بعد التعديل للربط بـ Gemini ---
async function generateResults() {
  const language = document.getElementById("language").value;
  const project = document.getElementById("projectName").value.trim();
  const service = document.getElementById("service").value.trim();
  const location = document.getElementById("location").value.trim();
  const industry = document.getElementById("industry").value.trim();
  const audience = document.getElementById("audience").value.trim();
  const seeds = document.getElementById("seedKeywords").value;
  const url = document.getElementById("url").value.trim();

  if (!project || !service) {
    showToast(language === "ar" ? "يرجى إدخال اسم المشروع والوصف" : "Please enter project name and description");
    return;
  }

  showLoader();
  updateDirection(language);

  try {
    // إرسال البيانات إلى Flask (app.py)
    const response = await fetch('/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        language, project, service, location, industry, audience, seeds, url
      })
    });

    const data = await response.json();

    if (data.success) {
      const res = data.data; // البيانات القادمة من Gemini

      // توزيع النتائج على المربعات في تصميمك
      renderList("primaryKeywords", res.primaryKeywords, "keyword");
      renderList("supportingKeywords", res.supportingKeywords, "keyword");
      renderList("slogans", res.slogans, "result-item");
      renderList("shortHeadlines", res.shortHeadlines, "result-item");
      renderList("longHeadlines", res.longHeadlines, "result-item");
      renderList("descriptions", res.descriptions, "result-item");
      renderList("contentIdeas", res.contentIdeas, "result-item");
      
      // تحديث أزرار الـ CTA
      document.getElementById("ctaButtons").innerHTML = 
        res.ctas.map(c => `<span class="cta">${c}</span>`).join("");

      // تحديث الإحصائيات في التصميم
      document.getElementById("statProject").textContent = project || "—";
      document.getElementById("statIndustry").textContent = industry || "—";
      document.getElementById("statLocation").textContent = location || "—";

      showToast(language === "ar" ? "تم التوليد بذكاء" : "Generated with AI");
    }
  } catch (error) {
    console.error("AI Error:", error);
    showToast("Error connecting to AI server");
  } finally {
    hideLoader();
  }
}

// دالة مساعدة لعرض القوائم بنفس ستايلك
function renderList(elementId, items, className) {
  const container = document.getElementById(elementId);
  if (container && items) {
    container.innerHTML = items.map(item => `<div class="${className}">${item}</div>`).join("");
  }
}

function copyContent(id) {
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text);
  showToast("Copied");
}

function resetResults() {
  document.getElementById("projectName").value = "";
  document.getElementById("service").value = "";
  document.getElementById("location").value = "";
  document.getElementById("industry").value = "";
  document.getElementById("audience").value = "";
  document.getElementById("seedKeywords").value = "";
  document.getElementById("url").value = "";
}

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

function renderList(elementId, items, className) {
  const container = document.getElementById(elementId);
  if (!container) return;
  if (!items || !items.length) {
    container.innerHTML = `<div class="empty">No results yet.</div>`;
    return;
  }
  container.innerHTML = items.map(item => {
    if (className === "keyword") {
      return `<span class="${className}">${item}</span>`;
    }
    return `<div class="${className}">${item}</div>`;
  }).join("");
}

function normalizeArray(value) {
  if (!value) return [];
  if (Array.isArray(value)) return value;
  return [value];
}

async function generateResults() {
  const language = document.getElementById("language").value;
  const project = document.getElementById("projectName").value.trim();
  const service = document.getElementById("service").value.trim();
  const country = document.getElementById("country").value.trim();
  const industry = document.getElementById("industry").value.trim();
  const audience = document.getElementById("audience").value.trim();
  const seeds = document.getElementById("seedKeywords").value.trim();
  const url = document.getElementById("url").value.trim();

  if (!project || !service || !country || !industry) {
    showToast(
      language === "ar"
        ? "يرجى إدخال اسم المشروع، الخدمة، الدولة، والمجال"
        : "Please enter project name, service, country, and industry"
    );
    return;
  }

  showLoader();
  updateDirection(language);

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        language,
        project,
        service,
        country,
        industry,
        audience,
        seeds,
        url,
        domain: extractDomain(url)
      })
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(data.error || "AI generation failed");
    }

    const res = data.data || {};

    renderList("primaryKeywords", normalizeArray(res.primaryKeywords), "keyword");
    renderList("supportingKeywords", normalizeArray(res.supportingKeywords), "keyword");
    renderList("slogans", normalizeArray(res.slogans), "result-item");
    renderList("shortHeadlines", normalizeArray(res.shortHeadlines), "result-item");
    renderList("longHeadlines", normalizeArray(res.longHeadlines), "result-item");
    renderList("descriptions", normalizeArray(res.descriptions), "result-item");
    renderList("contentIdeas", normalizeArray(res.contentIdeas), "result-item");

    const ctas = normalizeArray(res.ctas);
    document.getElementById("ctaButtons").innerHTML =
      ctas.length
        ? ctas.map(c => `<span class="cta">${c}</span>`).join("")
        : `<div class="empty">No CTA suggestions yet.</div>`;

    document.getElementById("statProject").textContent = project || "—";
    document.getElementById("statIndustry").textContent = industry || "—";
    document.getElementById("statCountry").textContent = country || "—";

    showToast(language === "ar" ? "تم التوليد بنجاح" : "Generated successfully");
  } catch (error) {
    console.error("AI Error:", error);
    showToast(language === "ar" ? "حدث خطأ في الاتصال بالسيرفر" : "Error connecting to AI server");
  } finally {
    hideLoader();
  }
}

function copyContent(id) {
  const element = document.getElementById(id);
  if (!element) return;
  const text = element.innerText.trim();
  if (!text) {
    showToast("Nothing to copy");
    return;
  }
  navigator.clipboard.writeText(text);
  showToast("Copied");
}

function resetResults() {
  document.getElementById("projectName").value = "";
  document.getElementById("service").value = "";
  document.getElementById("country").value = "";
  document.getElementById("industry").value = "";
  document.getElementById("audience").value = "";
  document.getElementById("seedKeywords").value = "";
  document.getElementById("url").value = "";

  document.getElementById("statProject").textContent = "—";
  document.getElementById("statIndustry").textContent = "—";
  document.getElementById("statCountry").textContent = "—";

  renderList("primaryKeywords", [], "keyword");
  renderList("supportingKeywords", [], "keyword");
  renderList("slogans", [], "result-item");
  renderList("shortHeadlines", [], "result-item");
  renderList("longHeadlines", [], "result-item");
  renderList("descriptions", [], "result-item");
  renderList("contentIdeas", [], "result-item");
  document.getElementById("ctaButtons").innerHTML = `<div class="empty">No CTA suggestions yet.</div>`;
}

resetResults();

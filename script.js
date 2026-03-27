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

  setTimeout(() => {
    toast.classList.remove("show");
  }, 1800);
}

function makeSmartKeywords(service, industry, audience, location, language, domain) {
  const s = service || (language === "ar" ? "الخدمة" : "service");
  const i = industry || (language === "ar" ? "المجال" : "industry");
  const a = audience || (language === "ar" ? "العملاء" : "customers");
  const l = location || "";
  const base = domain || s;

  if (language === "ar") {
    const primary = [
      `${base}`,
      `${s} في ${i}`,
      `${s} لـ ${a}`,
      `حلول ${i}`,
      l ? `${s} في ${l}` : `أفضل ${s}`,
      l ? `${i} في ${l}` : `${i} الرقمي`
    ];

    const lsi = [
      `استراتيجيات ${i}`,
      `تحسين الوصول للعملاء`,
      `زيادة المبيعات`,
      `حلول مبتكرة`,
      `نمو الأعمال`,
      `تحسين التحويل`,
      `بناء العلامة التجارية`,
      `استهداف ${a}`
    ];

    return { primary, lsi };
  }

  const primary = [
    `${base}`,
    `${s} for ${a}`,
    `${i} solutions`,
    `best ${s}`,
    l ? `${s} in ${l}` : `${s} online`,
    `${i} services`
  ];

  const lsi = [
    `${i} growth strategy`,
    `customer acquisition`,
    `conversion optimization`,
    `brand awareness`,
    `lead generation`,
    `${s} experts`,
    `${i} digital solutions`,
    `targeting ${a}`
  ];

  return { primary, lsi };
}

function makeAdCopy(project, service, industry, audience, location, language, domain) {
  if (language === "ar") {
    return {
      shortHeadlines: [
        domain ? `اكتشف ${domain}` : `طوّر ${project}`,
        `نمِّ أعمالك مع ${service}`,
        location ? `وسع وصولك في ${location}` : `وسع وصولك للعملاء`,
        `${industry} بطريقة أذكى`
      ],
      longHeadlines: [
        `${service} يساعد ${audience} على تحقيق نتائج أفضل ونمو أسرع.`,
        `ارتقِ في مجال ${industry} بحلول تسويقية أكثر ذكاءً وفعالية.`,
        `${project} يمنحك طريقة أفضل لجذب العملاء وتحويلهم إلى نتائج حقيقية.`
      ],
      ctas: [
        "ابدأ الآن",
        "اطلب عرضًا تجريبيًا",
        "تواصل معنا",
        "جرّب اليوم"
      ]
    };
  }

  return {
    shortHeadlines: [
      domain ? `Discover ${domain}` : `Boost ${project}`,
      `Grow with ${service}`,
      location ? `Reach more clients in ${location}` : `Reach more customers`,
      `${industry} made smarter`
    ],
    longHeadlines: [
      `Discover how ${service} helps ${audience} achieve faster growth.`,
      `Scale your ${industry} business with smarter, more effective marketing.`,
      `${project} gives you a better way to attract, engage, and convert customers.`
    ],
    ctas: [
      "Get Started",
      "Request Demo",
      "Contact Us",
      "Start Today"
    ]
  };
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

function generateResults() {
  showLoader();

  setTimeout(() => {
    const language = document.getElementById("language").value;
    const project =
      document.getElementById("projectName").value.trim() ||
      (language === "ar" ? "مشروعك" : "Your Project");
    const service =
      document.getElementById("service").value.trim() ||
      (language === "ar" ? "خدمتك" : "your service");
    const url = document.getElementById("url").value.trim();
    const domain = extractDomain(url);
    const location =
      document.getElementById("location").value.trim() ||
      (language === "ar" ? "سوقك" : "your market");
    const industry =
      document.getElementById("industry").value.trim() ||
      (language === "ar" ? "مجالك" : "your industry");
    const audience =
      document.getElementById("audience").value.trim() ||
      (language === "ar" ? "عملائك" : "your audience");

    updateDirection(language);

    const ads = makeAdCopy(
      project,
      service,
      industry,
      audience,
      location,
      language,
      domain
    );

    const keywordsData = makeSmartKeywords(
      service,
      industry,
      audience,
      location,
      language,
      domain
    );

    document.getElementById("statProject").textContent = project;
    document.getElementById("statIndustry").textContent = industry;
    document.getElementById("statLocation").textContent = location;

    document.getElementById("shortHeadlines").innerHTML = ads.shortHeadlines
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    document.getElementById("longHeadlines").innerHTML = ads.longHeadlines
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    document.getElementById("primaryKeywords").innerHTML = keywordsData.primary
      .map(item => `<span class="keyword">${item}</span>`)
      .join("");

    document.getElementById("lsiKeywords").innerHTML = keywordsData.lsi
      .map(item => `<span class="keyword">${item}</span>`)
      .join("");

    document.getElementById("ctaButtons").innerHTML = ads.ctas
      .map(item => `<span class="cta">${item}</span>`)
      .join("");

    hideLoader();
  }, 900);
}

function resetResults() {
  document.getElementById("projectName").value = "";
  document.getElementById("service").value = "";
  document.getElementById("url").value = "";
  document.getElementById("location").value = "";
  document.getElementById("industry").value = "";
  document.getElementById("audience").value = "";
  document.getElementById("language").value = "en";

  updateDirection("en");

  document.getElementById("statProject").textContent = "—";
  document.getElementById("statIndustry").textContent = "—";
  document.getElementById("statLocation").textContent = "—";

  document.getElementById("shortHeadlines").innerHTML =
    `<div class="empty">No headlines yet.</div>`;
  document.getElementById("longHeadlines").innerHTML =
    `<div class="empty">No long headlines yet.</div>`;
  document.getElementById("primaryKeywords").innerHTML =
    `<div class="empty">No keywords yet.</div>`;
  document.getElementById("lsiKeywords").innerHTML =
    `<div class="empty">No LSI keywords yet.</div>`;
  document.getElementById("ctaButtons").innerHTML =
    `<div class="empty">No CTA suggestions yet.</div>`;
}

function copyContent(elementId) {
  const element = document.getElementById(elementId);
  const text = element.innerText.trim();

  if (!text) {
    showToast("Nothing to copy");
    return;
  }

  navigator.clipboard.writeText(text)
    .then(() => showToast("Copied successfully"))
    .catch(() => showToast("Copy failed"));
}

resetResults();

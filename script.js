function showLoader() {
  document.getElementById("loader").classList.remove("hidden");
}

function hideLoader() {
  document.getElementById("loader").classList.add("hidden");
}

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 1800);
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


function extractDomain(url) {
  try {
    const parsed = new URL(url);
    return parsed.hostname.replace("www.", "");
  } catch {
    return "";
  }
}

function parseSeedKeywords(seedText) {
  return seedText
    .split(",")
    .map(k => k.trim())
    .filter(Boolean);
}

function uniqueList(items) {
  return [...new Set(items.filter(Boolean))];
}

function localizeIndustry(industry, language) {
  const map = {
    "Food / Cooking": { ar: "الطبخ والأكل", en: "Food & Cooking" },
    "Podcast / Storytelling": { ar: "البودكاست والحكايات", en: "Podcast & Storytelling" },
    "Audiobooks / Books": { ar: "الكتب المسموعة والكتب", en: "Audiobooks & Books" },
    "Sports": { ar: "الرياضة", en: "Sports" },
    "Health / Wellness": { ar: "الصحة والعافية", en: "Health & Wellness" },
    "Beauty": { ar: "الجمال", en: "Beauty" },
    "Kids": { ar: "الأطفال", en: "Kids" },
    "Education": { ar: "التعليم", en: "Education" },
    "Technology": { ar: "التقنية", en: "Technology" },
    "Retail": { ar: "التجزئة", en: "Retail" },
    "Finance": { ar: "المال والأعمال", en: "Finance" },
    "Travel": { ar: "السفر", en: "Travel" }
  };

  if (!map[industry]) {
    return language === "ar" ? "المحتوى" : "Content";
  }

  return map[industry][language];
}

function localizePlatform(platformType, language) {
  const map = {
    "Website": { ar: "موقع", en: "website" },
    "Mobile App": { ar: "تطبيق", en: "app" },
    "SaaS Platform": { ar: "منصة رقمية", en: "digital platform" },
    "E-commerce": { ar: "متجر إلكتروني", en: "e-commerce platform" },
    "Media Platform": { ar: "منصة إعلامية", en: "media platform" }
  };

  if (!map[platformType]) {
    return language === "ar" ? "منصة" : "platform";
  }

  return map[platformType][language];
}


function detectAudienceSignals(audience, language) {

  const text = (audience || "").toLowerCase();
  const signals = [];

  if (language === "ar") {

    if (text.includes("مواصلات") || text.includes("الطريق"))
      signals.push("commute");

    if (text.includes("ربة منزل") || text.includes("البيت"))
      signals.push("home");

    if (text.includes("كبار"))
      signals.push("older");

    if (text.includes("شباب") || text.includes("طلاب"))
      signals.push("youth");

    if (text.includes("يسمع") || text.includes("صوت"))
      signals.push("listening");

  } else {

    if (text.includes("commute") || text.includes("road"))
      signals.push("commute");

    if (text.includes("home"))
      signals.push("home");

    if (text.includes("older") || text.includes("seniors"))
      signals.push("older");

    if (text.includes("youth") || text.includes("students"))
      signals.push("youth");

    if (text.includes("listen") || text.includes("audio"))
      signals.push("listening");

  }

  return uniqueList(signals);
}


function buildAudienceHooks(signals, language) {

  const hooks = [];

  if (language === "ar") {

    if (signals.includes("commute"))
      hooks.push("استمع واستمتع بالطريق", "رفيقك اليومي في المواصلات");

    if (signals.includes("home"))
      hooks.push("استمع وأنت في البيت", "محتوى يرافق يومك في المنزل");

    if (signals.includes("older"))
      hooks.push("محتوى مريح للكبار");

  } else {

    if (signals.includes("commute"))
      hooks.push("Listen and enjoy the road");

    if (signals.includes("home"))
      hooks.push("Content that fits your day at home");

    if (signals.includes("older"))
      hooks.push("Comfortable listening for older audiences");

  }

  return uniqueList(hooks);
}


function makeSeoKeywords(
  language,
  project,
  service,
  industry,
  platform,
  seeds,
  audience,
  location,
  domain
) {

  const base = domain || project || service || industry;

  const primary = [];
  const supporting = [];

  primary.push(
    base,
    industry,
    service,
    `${platform} ${industry}`
  );

  primary.push(...seeds);

  if (audience) {
    primary.push(
      language === "ar"
        ? `${industry} لـ ${audience}`
        : `${industry} for ${audience}`
    );
  }

  if (location) {
    primary.push(
      language === "ar"
        ? `${industry} في ${location}`
        : `${industry} in ${location}`
    );
  }

  if (language === "ar") {

    supporting.push(
      "تحسين محركات البحث",
      "ظهور عضوي",
      `كلمات مفتاحية ${industry}`
    );

  } else {

    supporting.push(
      "search engine optimization",
      "organic visibility",
      `${industry} keywords`
    );

  }

  return {
    primary: uniqueList(primary).slice(0, 12),
    supporting: uniqueList(supporting).slice(0, 12)
  };
}


function generateResults() {

  showLoader();

  setTimeout(() => {

    const language = document.getElementById("language").value;

    const project =
      document.getElementById("projectName").value.trim();

    const url =
      document.getElementById("url").value.trim();

    const domain = extractDomain(url);

    const platformType =
      document.getElementById("platformType").value.trim();

    const service =
      document.getElementById("service").value.trim();

   const location =
document.getElementById("location").value;

    const industry =
      document.getElementById("industry").value.trim();

    const audience =
      document.getElementById("audience").value.trim();

    const seeds = parseSeedKeywords(
      document.getElementById("seedKeywords").value
    );

    updateDirection(language);

    const localizedIndustry =
      localizeIndustry(industry, language);

    const platformLabel =
      localizePlatform(platformType, language);

    const audienceSignals =
      detectAudienceSignals(audience, language);

    const audienceHooks =
      buildAudienceHooks(audienceSignals, language);

    const seo =
      makeSeoKeywords(
        language,
        project,
        service,
        localizedIndustry,
        platformLabel,
        seeds,
        audience,
        location,
        domain
      );

    /* === Update UI === */

    document.getElementById("statProject").textContent =
      project || "—";

    document.getElementById("statIndustry").textContent =
      localizedIndustry || "—";

    document.getElementById("statLocation").textContent =
      location || "—";

    document.getElementById("primaryKeywords").innerHTML =
      seo.primary
        .map(k => `<span class="keyword">${k}</span>`)
        .join("");

    document.getElementById("supportingKeywords").innerHTML =
      seo.supporting
        .map(k => `<span class="keyword">${k}</span>`)
        .join("");

    hideLoader();

  }, 500);
}

/* =========================
   RESET
========================= */

function resetResults() {

  document.getElementById("projectName").value = "";
  document.getElementById("url").value = "";
  document.getElementById("service").value = "";
  document.getElementById("location").value = "";
  document.getElementById("audience").value = "";
  document.getElementById("seedKeywords").value = "";

}

/* =========================
   COPY FUNCTION
========================= */

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

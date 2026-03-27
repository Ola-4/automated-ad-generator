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
  setTimeout(() => toast.classList.remove("show"), 2000);
}

function updateDirection(language) {
  if (language === "ar") {
    document.body.setAttribute("dir", "rtl");
  } else {
    document.body.setAttribute("dir", "ltr");
  }
}

function parseKeywords(text) {
  return text
    .split(",")
    .map(k => k.trim())
    .filter(k => k.length > 0);
}

function generateResults() {

  showLoader();

  setTimeout(() => {

    const language = document.getElementById("language").value;
    const project = document.getElementById("projectName").value.trim();
    const industry = document.getElementById("industry").value.trim();
    const audience = document.getElementById("audience").value.trim();
    const keywords = parseKeywords(document.getElementById("seedKeywords").value);

    updateDirection(language);

    if (!industry || keywords.length === 0) {
      hideLoader();
      alert("Please select industry and add keywords.");
      return;
    }

    generateSEO(language, industry, keywords);
    generateSlogans(language, project, industry);
    generateHeadlines(language, industry, keywords, audience);
    generateDescriptions(language, industry, audience);
    generateCTA(language);
    generateIdeas(language, industry, keywords);

    hideLoader();

  }, 500);
}


function generateSEO(language, industry, keywords) {

  let primary = keywords.slice(0, 10);

  let support = [];

  if (language === "ar") {

    support = [
      "تحسين محركات البحث",
      "الظهور في جوجل",
      `محتوى ${industry}`,
      "زيادة الزيارات",
      "نمو الموقع",
      "الوصول للجمهور"
    ];

  } else {

    support = [
      "SEO strategy",
      "organic traffic",
      `${industry} content`,
      "search ranking",
      "content marketing",
      "audience growth"
    ];

  }

  document.getElementById("primaryKeywords").innerHTML =
    primary.map(k => `<span class="keyword">${k}</span>`).join("");

  document.getElementById("supportingKeywords").innerHTML =
    support.map(k => `<span class="keyword">${k}</span>`).join("");
}


function generateSlogans(language, project, industry) {

  let slogans = [];

  if (language === "ar") {

    slogans = [
      `${project} أقرب ليك`,
      "محتوى يرافق يومك",
      "اكتشف الأفضل",
      `استمتع بـ ${industry}`,
      "ابدأ التجربة الآن",
      "أفكار تلهمك",
      "استمع واستمتع",
      "محتوى أقرب للحياة",
      "قصص تستحق السماع",
      "ابدأ الآن"
    ];

  } else {

    slogans = [
      `${project} closer to you`,
      "Content for your day",
      "Discover something new",
      `Explore ${industry}`,
      "Start your experience",
      "Ideas that inspire",
      "Listen and enjoy",
      "Content for real life",
      "Stories worth hearing",
      "Start today"
    ];

  }

  document.getElementById("slogans").innerHTML =
    slogans.map(s => `<div class="result-item">${s}</div>`).join("");
}


function generateHeadlines(language, industry, keywords, audience) {

  let short = [];
  let long = [];

  if (language === "ar") {

    short = [
      `اكتشف ${industry}`,
      `أفضل ${keywords[0]}`,
      `محتوى ${industry}`,
      `ابدأ مع ${industry}`,
      `استمتع الآن`,
      `محتوى يناسبك`,
      `الأفضل لك`,
      `جرب الآن`,
      `اكتشف أكثر`,
      `محتوى جديد`
    ];

    long = [
      `اكتشف تجربة جديدة في ${industry}`,
      `محتوى ${industry} يناسب ${audience}`,
      `استمتع بمحتوى حول ${keywords[0]}`,
      `أفضل تجربة ${industry}`,
      `محتوى يواكب اهتماماتك`,
      `استكشف عالم ${industry}`,
      `محتوى يلهم يومك`,
      `ابدأ رحلتك مع ${industry}`,
      `أفضل محتوى ${industry}`,
      `اكتشف الأفضل الآن`
    ];

  } else {

    short = [
      `Discover ${industry}`,
      `Best ${keywords[0]}`,
      `${industry} content`,
      `Start today`,
      `Explore now`,
      `Something new`,
      `Better content`,
      `Try it today`,
      `Discover more`,
      `New experience`
    ];

    long = [
      `Discover a better ${industry} experience`,
      `${industry} content for ${audience}`,
      `Explore content about ${keywords[0]}`,
      `The best ${industry} experience`,
      `Content that fits your interests`,
      `Explore the world of ${industry}`,
      `Content that inspires your day`,
      `Start your journey today`,
      `Discover great content`,
      `Experience something new`
    ];

  }

  document.getElementById("shortHeadlines").innerHTML =
    short.map(s => `<div class="result-item">${s}</div>`).join("");

  document.getElementById("longHeadlines").innerHTML =
    long.map(s => `<div class="result-item">${s}</div>`).join("");
}


function generateDescriptions(language, industry, audience) {

  let desc = [];

  if (language === "ar") {

    desc = [
      `محتوى ${industry} يناسب اهتماماتك.`,
      `منصة تقدم أفضل محتوى ${industry}.`,
      `استمتع بتجربة جديدة في ${industry}.`,
      `محتوى مناسب لـ ${audience}.`,
      `استكشف أفكارًا جديدة يوميًا.`,
      `محتوى يلهمك ويقربك من اهتماماتك.`,
      `أفضل تجربة محتوى.`,
      `اكتشف المزيد الآن.`,
      `محتوى بسيط وممتع.`,
      `ابدأ التجربة الآن.`
    ];

  } else {

    desc = [
      `${industry} content built for your interests.`,
      `Discover a new ${industry} experience.`,
      `Content designed for ${audience}.`,
      `Explore ideas every day.`,
      `Simple and engaging content.`,
      `Content that inspires.`,
      `Discover something new.`,
      `Start today.`,
      `Better content experience.`,
      `Enjoy the journey.`
    ];

  }

  document.getElementById("descriptions").innerHTML =
    desc.map(d => `<div class="result-item">${d}</div>`).join("");
}


function generateCTA(language) {

  let ctas = language === "ar"
    ? ["ابدأ الآن", "اكتشف المزيد", "جرب اليوم", "استمع الآن", "استكشف المحتوى", "ابدأ التجربة", "شاهد الآن", "تعرف أكثر", "ابدأ اليوم", "انضم الآن"]
    : ["Start Now", "Discover More", "Try Today", "Listen Now", "Explore Content", "Get Started", "See More", "Learn More", "Join Now", "Start Today"];

  document.getElementById("ctaButtons").innerHTML =
    ctas.map(c => `<span class="cta">${c}</span>`).join("");
}


function generateIdeas(language, industry, keywords) {

  let ideas = [];

  if (language === "ar") {

    ideas = [
      `محتوى حول ${keywords[0]}`,
      `أفضل أفكار ${industry}`,
      `مواضيع قريبة من الجمهور`,
      `محتوى تعليمي`,
      `محتوى ملهم`,
      `محتوى يومي`,
      `قصص وتجارب`,
      `أفكار جديدة`,
      `محتوى بسيط`,
      `أفضل المواضيع`
    ];

  } else {

    ideas = [
      `Content about ${keywords[0]}`,
      `${industry} ideas`,
      "Audience focused content",
      "Educational content",
      "Inspiring topics",
      "Daily content",
      "Stories and experiences",
      "Fresh ideas",
      "Simple content",
      "Trending topics"
    ];

  }

  document.getElementById("contentIdeas").innerHTML =
    ideas.map(i => `<div class="result-item">${i}</div>`).join("");
}


function copyContent(id) {

  const text = document.getElementById(id).innerText;

  navigator.clipboard.writeText(text);

  showToast("Copied");
}


function resetResults() {

  document.getElementById("projectName").value = "";
  document.getElementById("industry").value = "";
  document.getElementById("audience").value = "";
  document.getElementById("seedKeywords").value = "";

  document.getElementById("primaryKeywords").innerHTML = "";
  document.getElementById("supportingKeywords").innerHTML = "";
  document.getElementById("slogans").innerHTML = "";
  document.getElementById("shortHeadlines").innerHTML = "";
  document.getElementById("longHeadlines").innerHTML = "";
  document.getElementById("descriptions").innerHTML = "";
  document.getElementById("ctaButtons").innerHTML = "";
  document.getElementById("contentIdeas").innerHTML = "";

}

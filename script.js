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

function generateResults() {

  showLoader();

  setTimeout(() => {

    const language = document.getElementById("language").value;

    const project = document.getElementById("projectName").value.trim();

    const service = document.getElementById("service").value.trim();

    const location = document.getElementById("location").value.trim();

    const industry = document.getElementById("industry").value.trim();

    const audience = document.getElementById("audience").value.trim();

    const seeds = parseSeedKeywords(
      document.getElementById("seedKeywords").value
    );

    const url = document.getElementById("url").value.trim();

    const domain = extractDomain(url);

    updateDirection(language);

    const base = domain || project || service || industry;

    generateSEO(language, base, industry, seeds);

    generateSlogans(language, base);

    generateHeadlines(language, base, industry, seeds, audience);

    generateDescriptions(language, base, industry, audience);

    generateCTA(language);

    generateIdeas(language, industry, seeds);

    document.getElementById("statProject").textContent =
      project || "—";

    document.getElementById("statIndustry").textContent =
      industry || "—";

    document.getElementById("statLocation").textContent =
      location || "—";

    hideLoader();

  }, 500);
}


function generateSEO(language, base, industry, keywords) {

  let primary = uniqueList([
    base,
    industry,
    ...keywords
  ]).slice(0,10);

  let support;

  if(language==="ar"){

    support = [
      "تحسين محركات البحث",
      "الظهور في جوجل",
      `محتوى ${industry}`,
      "زيادة الزيارات",
      "نمو الموقع",
      "الوصول للجمهور"
    ];

  }else{

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
    primary.map(k=>`<span class="keyword">${k}</span>`).join("");

  document.getElementById("supportingKeywords").innerHTML =
    support.map(k=>`<span class="keyword">${k}</span>`).join("");
}



function generateSlogans(language, name){

  let slogans;

  if(language==="ar"){

    slogans = [
      `${name} أقرب ليك`,
      "محتوى يرافق يومك",
      "استمع واستمتع",
      "من الطريق إلى البيت",
      "أفكار تلهمك",
      "ابدأ الآن",
      "اكتشف الأفضل",
      "قصص تستحق السماع",
      "محتوى أقرب للحياة",
      "كل يوم تجربة"
    ];

  }else{

    slogans = [
      `${name} closer to you`,
      "Content for your day",
      "Listen and enjoy",
      "Discover something new",
      "Ideas that inspire",
      "Start now",
      "Explore the experience",
      "Stories worth hearing",
      "Content for real life",
      "Every day something new"
    ];

  }

  document.getElementById("slogans").innerHTML =
    slogans.map(s=>`<div class="result-item">${s}</div>`).join("");

}



function generateHeadlines(language, base, industry, keywords, audience){

  let short;
  let long;

  if(language==="ar"){

    short = [
      `اكتشف ${industry}`,
      `أفضل ${keywords[0]||industry}`,
      `محتوى ${industry}`,
      `ابدأ مع ${base}`,
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
      `استمتع بمحتوى حول ${keywords[0]||industry}`,
      `أفضل تجربة ${industry}`,
      `محتوى يواكب اهتماماتك`,
      `استكشف عالم ${industry}`,
      `محتوى يلهم يومك`,
      `ابدأ رحلتك مع ${base}`,
      `أفضل محتوى ${industry}`,
      `اكتشف الأفضل الآن`
    ];

  }else{

    short = [
      `Discover ${industry}`,
      `Best ${keywords[0]||industry}`,
      `${industry} content`,
      `Start with ${base}`,
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
      `Explore content about ${keywords[0]||industry}`,
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
    short.map(s=>`<div class="result-item">${s}</div>`).join("");

  document.getElementById("longHeadlines").innerHTML =
    long.map(s=>`<div class="result-item">${s}</div>`).join("");

}



function generateDescriptions(language, base, industry, audience){

  let desc;

  if(language==="ar"){

    desc = [
      `${base} يقدم محتوى في ${industry}.`,
      `استمتع بتجربة جديدة في ${industry}.`,
      `محتوى مناسب لـ ${audience}.`,
      `استكشف أفكارًا جديدة يوميًا.`,
      `محتوى يلهمك.`,
      `أفضل تجربة محتوى.`,
      `اكتشف المزيد الآن.`,
      `محتوى بسيط وممتع.`,
      `ابدأ التجربة الآن.`,
      `محتوى يناسب اهتماماتك.`
    ];

  }else{

    desc = [
      `${base} delivers ${industry} content.`,
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
    desc.map(d=>`<div class="result-item">${d}</div>`).join("");

}



function generateCTA(language){

  const ctas = language==="ar"
  ?["ابدأ الآن","اكتشف المزيد","جرب اليوم","استمع الآن","استكشف المحتوى","ابدأ التجربة","شاهد الآن","تعرف أكثر","ابدأ اليوم","انضم الآن"]
  :["Start Now","Discover More","Try Today","Listen Now","Explore Content","Get Started","See More","Learn More","Join Now","Start Today"];

  document.getElementById("ctaButtons").innerHTML =
    ctas.map(c=>`<span class="cta">${c}</span>`).join("");

}



function generateIdeas(language,industry,keywords){

  let ideas;

  if(language==="ar"){

    ideas = [
      `محتوى حول ${keywords[0]||industry}`,
      `أفضل أفكار ${industry}`,
      "مواضيع قريبة من الجمهور",
      "محتوى تعليمي",
      "محتوى ملهم",
      "محتوى يومي",
      "قصص وتجارب",
      "أفكار جديدة",
      "محتوى بسيط",
      "أفضل المواضيع"
    ];

  }else{

    ideas = [
      `Content about ${keywords[0]||industry}`,
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
    ideas.map(i=>`<div class="result-item">${i}</div>`).join("");

}



function copyContent(id){

  const text=document.getElementById(id).innerText;

  navigator.clipboard.writeText(text);

  showToast("Copied");

}



function resetResults(){

  document.getElementById("projectName").value="";
  document.getElementById("service").value="";
  document.getElementById("location").value="";
  document.getElementById("industry").value="";
  document.getElementById("audience").value="";
  document.getElementById("seedKeywords").value="";

}

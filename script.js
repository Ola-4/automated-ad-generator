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

  if (!map[industry]) return language === "ar" ? "المحتوى" : "Content";
  return language === "ar" ? map[industry].ar : map[industry].en;
}

function detectAudienceSignals(audience, language) {
  const text = (audience || "").toLowerCase();
  const signals = [];

  if (language === "ar") {
    if (text.includes("مواصلات") || text.includes("الطريق") || text.includes("مشوار")) signals.push("commute");
    if (text.includes("ربة منزل") || text.includes("ربات المنزل") || text.includes("البيت") || text.includes("المنزل")) signals.push("home");
    if (text.includes("كبار") || text.includes("الكبار") || text.includes("كبار السن")) signals.push("older");
    if (text.includes("شباب") || text.includes("طلاب") || text.includes("المراهق")) signals.push("youth");
    if (text.includes("يسمع") || text.includes("استماع") || text.includes("صوت") || text.includes("يسمعوا")) signals.push("listening");
    if (text.includes("مشغول") || text.includes("مشغولين") || text.includes("زحمة")) signals.push("busy");
    if (text.includes("عائلات") || text.includes("أسر")) signals.push("family");
    if (text.includes("يحب") || text.includes("يحبوا") || text.includes("يفضل")) signals.push("interest");
  } else {
    if (text.includes("commute") || text.includes("road") || text.includes("transport") || text.includes("driving")) signals.push("commute");
    if (text.includes("home") || text.includes("housewives") || text.includes("household")) signals.push("home");
    if (text.includes("older") || text.includes("elderly") || text.includes("seniors")) signals.push("older");
    if (text.includes("youth") || text.includes("young") || text.includes("students")) signals.push("youth");
    if (text.includes("listen") || text.includes("audio") || text.includes("hearing")) signals.push("listening");
    if (text.includes("busy")) signals.push("busy");
    if (text.includes("family") || text.includes("families")) signals.push("family");
    if (text.includes("love") || text.includes("prefer") || text.includes("enjoy")) signals.push("interest");
  }

  return uniqueList(signals);
}

function buildAudienceHooks(signals, language) {
  if (language === "ar") {
    const hooks = [];

    if (signals.includes("commute")) {
      hooks.push("استمع واستمتع بالطريق");
      hooks.push("رفيقك اليومي في المواصلات");
    }
    if (signals.includes("home")) {
      hooks.push("استمع وأنت في البيت");
      hooks.push("محتوى يرافق يومك في المنزل");
    }
    if (signals.includes("older")) {
      hooks.push("محتوى سهل ومريح للكبار");
      hooks.push("استماع هادئ يناسب كل الأعمار");
    }
    if (signals.includes("busy")) {
      hooks.push("محتوى يناسب يومك المشغول");
      hooks.push("استمع في أي وقت بدون تعقيد");
    }
    if (signals.includes("listening")) {
      hooks.push("محتوى صُمم لعشاق الاستماع");
      hooks.push("استماع ممتع في كل لحظة");
    }
    if (signals.includes("family")) {
      hooks.push("محتوى قريب من العائلة");
    }
    if (signals.includes("youth")) {
      hooks.push("محتوى قريب من الشباب");
    }
    if (signals.includes("interest")) {
      hooks.push("محتوى أقرب لاهتمامات جمهورك");
    }

    return uniqueList(hooks);
  }

  const hooks = [];

  if (signals.includes("commute")) {
    hooks.push("Listen and enjoy the road");
    hooks.push("Your daily companion on the commute");
  }
  if (signals.includes("home")) {
    hooks.push("Enjoy it while at home");
    hooks.push("Content that fits your day at home");
  }
  if (signals.includes("older")) {
    hooks.push("Comfortable listening for older audiences");
    hooks.push("Simple and warm content for every age");
  }
  if (signals.includes("busy")) {
    hooks.push("Content made for busy days");
    hooks.push("Listen anytime without effort");
  }
  if (signals.includes("listening")) {
    hooks.push("Built for people who love listening");
    hooks.push("Audio enjoyment in every moment");
  }
  if (signals.includes("family")) {
    hooks.push("Content that fits family life");
  }
  if (signals.includes("youth")) {
    hooks.push("A tone that connects with younger audiences");
  }
  if (signals.includes("interest")) {
    hooks.push("Content built around audience interests");
  }

  return uniqueList(hooks);
}

function localizePlatform(platformType, language) {
  const map = {
    "Portal": { ar: "منصة", en: "platform" },
    "Website": { ar: "موقع", en: "website" },
    "Mobile App": { ar: "تطبيق", en: "app" },
    "SaaS Platform": { ar: "منصة رقمية", en: "digital platform" },
    "E-commerce": { ar: "متجر إلكتروني", en: "e-commerce platform" },
    "Media Platform": { ar: "منصة إعلامية", en: "media platform" }
  };

  if (!map[platformType]) return language === "ar" ? "منصة" : "platform";
  return language === "ar" ? map[platformType].ar : map[platformType].en;
}

function makeSeoKeywords(language, project, service, localizedIndustry, platformLabel, seeds, audience, location, domain) {
  const baseName = domain || project || service || localizedIndustry;
  const primary = [];
  const supporting = [];

  primary.push(baseName);
  primary.push(localizedIndustry);
  primary.push(service || "");
  primary.push(`${platformLabel} ${localizedIndustry}`);
  if (audience) primary.push(language === "ar" ? `${localizedIndustry} لـ ${audience}` : `${localizedIndustry} for ${audience}`);
  if (location) primary.push(language === "ar" ? `${localizedIndustry} في ${location}` : `${localizedIndustry} in ${location}`);
  primary.push(...seeds);

  if (language === "ar") {
    supporting.push(
      "تحسين محركات البحث",
      "ظهور عضوي",
      `كلمات مفتاحية ${localizedIndustry}`,
      "نمو العلامة التجارية",
      "الوصول للجمهور",
      `محتوى ${localizedIndustry}`
    );
    if (audience) supporting.push(`اهتمامات ${audience}`);
    if (location) supporting.push(`${localizedIndustry} ${location}`);
  } else {
    supporting.push(
      "search engine optimization",
      "organic visibility",
      `${localizedIndustry} keywords`,
      "brand growth",
      "audience reach",
      `${localizedIndustry} content`
    );
    if (audience) supporting.push(`${audience} interests`);
    if (location) supporting.push(`${localizedIndustry} ${location}`);
  }

  return {
    primary: uniqueList(primary).slice(0, 12),
    supporting: uniqueList(supporting).slice(0, 12)
  };
}

function buildBrandMessage(language, project, platformLabel, localizedIndustry, audience, hooks, domain) {
  const name = domain || project || (language === "ar" ? "مشروعك" : "Your Project");
  const lines = [];

  if (language === "ar") {
    lines.push(`${name} ${platformLabel} يقدم محتوى في ${localizedIndustry} برسالة أقرب للجمهور.`);
    if (audience) lines.push(`موجه إلى ${audience}.`);
    if (hooks.length) {
      lines.push(...hooks.slice(0, 2));
    } else {
      lines.push("محتوى مفيد، قريب، وسهل الارتباط به.");
    }
    return uniqueList(lines);
  }

  lines.push(`${name} is a ${platformLabel} focused on ${localizedIndustry} with a message that feels closer to the audience.`);
  if (audience) lines.push(`Built for ${audience}.`);
  if (hooks.length) {
    lines.push(...hooks.slice(0, 2));
  } else {
    lines.push("Useful, relevant content with stronger audience connection.");
  }
  return uniqueList(lines);
}

function buildSeoTitle(language, project, localizedIndustry, seeds, domain) {
  const name = domain || project || (language === "ar" ? "مشروعك" : "Your Project");
  const seed = seeds[0] || "";

  if (language === "ar") {
    return seed
      ? `${name} | ${seed} | ${localizedIndustry}`
      : `${name} | ${localizedIndustry} | محتوى مفيد وملهم`;
  }

  return seed
    ? `${name} | ${seed} | ${localizedIndustry}`
    : `${name} | ${localizedIndustry} | Useful & Inspiring Content`;
}

function buildMetaDescription(language, project, localizedIndustry, audience, hooks, seeds, location, domain) {
  const name = domain || project || (language === "ar" ? "مشروعك" : "Your Project");
  const mainHook = hooks[0] || "";
  const topSeeds = seeds.slice(0, 4);

  if (language === "ar") {
    return `${name} منصة في ${localizedIndustry}${audience ? ` موجهة إلى ${audience}` : ""}${location ? ` في ${location}` : ""}${mainHook ? `، ${mainHook}` : ""}${topSeeds.length ? `، مع تركيز على ${topSeeds.join("، ")}` : ""}.`;
  }

  return `${name} is a ${localizedIndustry} platform${audience ? ` built for ${audience}` : ""}${location ? ` in ${location}` : ""}${mainHook ? `, ${mainHook}` : ""}${topSeeds.length ? `, focused on ${topSeeds.join(", ")}` : ""}.`;
}

function buildShortHeadlines(language, project, localizedIndustry, hooks, seeds, domain, audience) {
  const name = domain || project || (language === "ar" ? "مشروعك" : "Your Project");
  const seedA = seeds[0] || localizedIndustry;
  const seedB = seeds[1] || "";
  const headlines = [];

  if (language === "ar") {
    headlines.push(
      hooks[0] || `اكتشف ${name}`,
      hooks[1] || `${localizedIndustry} أقرب ليك`,
      `${name} - محتوى يناسب يومك`,
      `استمع أو استكشف ${seedA}`,
      seedB ? `${seedA} و${seedB}` : `${localizedIndustry} بروح مختلفة`,
      `محتوى ${localizedIndustry} أقرب للجمهور`,
      audience ? `${localizedIndustry} لـ ${audience}` : `${localizedIndustry} بشكل أذكى`,
      `ابدأ مع ${name}`,
      `اكتشف تجربة ${localizedIndustry}`,
      `محتوى يلامس يومك`
    );
  } else {
    headlines.push(
      hooks[0] || `Discover ${name}`,
      hooks[1] || `${localizedIndustry} that feels closer`,
      `${name} - content that fits your day`,
      `Explore ${seedA}`,
      seedB ? `${seedA} and ${seedB}` : `${localizedIndustry} with a better angle`,
      `${localizedIndustry} with stronger audience value`,
      audience ? `${localizedIndustry} for ${audience}` : `${localizedIndustry} made smarter`,
      `Start with ${name}`,
      `Discover ${localizedIndustry}`,
      `Content that fits your everyday life`
    );
  }

  return uniqueList(headlines).slice(0, 10);
}

function buildLongHeadlines(language, project, localizedIndustry, hooks, seeds, domain, location) {
  const name = domain || project || (language === "ar" ? "مشروعك" : "Your Project");
  const topSeeds = seeds.slice(0, 3);
  const headlines = [];

  if (language === "ar") {
    headlines.push(
      `${name} يقدم محتوى في ${localizedIndustry} بأسلوب أقرب وأكثر ارتباطًا بالجمهور.`,
      hooks[0] ? `${hooks[0]} مع محتوى يجمع بين الفائدة والمتعة.` : `اكتشف تجربة محتوى أذكى وأقرب ليومك.`,
      topSeeds.length ? `استمتع بمحتوى حول ${topSeeds.join("، ")}.` : `محتوى ملهم ومفيد يناسب لحظات يومك المختلفة.`,
      location ? `قدّم حضورًا أقوى في ${location} عبر محتوى ${localizedIndustry}.` : `قدّم محتوى ${localizedIndustry} برسالة أوضح.`,
      `محتوى صُمم ليكون أسهل في الوصول وأقرب للاهتمامات.`,
      `تجربة محتوى أكثر قربًا، ووضوحًا، وارتباطًا بالحياة اليومية.`,
      `${name} يجعل ${localizedIndustry} أكثر بساطة وجاذبية.`,
      `رسالة أقوى ومحتوى يعرف كيف يتحدث إلى الجمهور.`,
      `منصة تفهم اهتمامات الجمهور وتحوّلها إلى محتوى أقرب.`,
      `اكتشف محتوى يرافق يومك في البيت، الطريق، واللحظات الهادئة.`
    );
  } else {
    headlines.push(
      `${name} delivers ${localizedIndustry} in a way that feels closer and more relevant to the audience.`,
      hooks[0] ? `${hooks[0]} with content that blends value and enjoyment.` : `Discover a smarter content experience built for everyday moments.`,
      topSeeds.length ? `Explore content around ${topSeeds.join(", ")}.` : `Useful and inspiring content built for different parts of the day.`,
      location ? `Build a stronger presence in ${location} through ${localizedIndustry} content.` : `Deliver ${localizedIndustry} with a clearer and stronger message.`,
      `Content designed to feel more useful, accessible, and audience-friendly.`,
      `A content experience that feels closer, clearer, and more human.`,
      `${name} makes ${localizedIndustry} simpler and more engaging.`,
      `Stronger messaging and content that actually speaks to people.`,
      `A platform that understands audience interests and turns them into content.`,
      `Discover content that fits the road, home, and quieter parts of the day.`
    );
  }

  return uniqueList(headlines).slice(0, 10);
}

function buildDescriptions(language, project, localizedIndustry, hooks, seeds, audience, domain) {
  const name = domain || project || (language === "ar" ? "مشروعك" : "Your Project");
  const topSeeds = seeds.slice(0, 4);
  const descriptions = [];

  if (language === "ar") {
    descriptions.push(
      `${name} يقدم محتوى في ${localizedIndustry} يناسب اهتمامات جمهورك ويقرب الرسالة منهم.`,
      hooks[0] || `محتوى في ${localizedIndustry} أقرب للحياة اليومية.`,
      topSeeds.length ? `محتوى مبني حول ${topSeeds.join("، ")}.` : `محتوى يركز على القيمة والفائدة.`,
      audience ? `مصمم ليستجيب لاحتياجات ${audience}.` : `مصمم ليكون أقرب للجمهور.`,
      `تجربة بسيطة، واضحة، وسهلة الارتباط بها.`,
      `رسائل أقوى تساعدك في الظهور العضوي والإعلانات.`,
      `منصة تساعدك على تحويل الكلمات المفتاحية إلى جمل مؤثرة.`,
      `محتوى أقرب للناس، وأسهل في الاستهلاك، وأكثر قابلية للتذكر.`,
      `أسلوب يناسب الطريق، البيت، والانشغال اليومي.`,
      `استخدم جمهورك وكلماتك المفتاحية للحصول على نتائج أقرب للواقع.`
    );
  } else {
    descriptions.push(
      `${name} delivers ${localizedIndustry} content that feels more relevant to your audience.`,
      hooks[0] || `${localizedIndustry} content made for everyday life.`,
      topSeeds.length ? `Built around ${topSeeds.join(", ")}.` : `Focused on usefulness and value.`,
      audience ? `Designed to respond to the needs of ${audience}.` : `Built to feel closer to real audiences.`,
      `A simple, clearer, and more relatable content experience.`,
      `Stronger messaging for both organic growth and campaigns.`,
      `A platform that helps turn keywords into meaningful copy.`,
      `Content that feels easier to consume and easier to remember.`,
      `A tone that fits the road, home, and busy daily routines.`,
      `Use your audience and your keywords to generate more realistic output.`
    );
  }

  return uniqueList(descriptions).slice(0, 10);
}

function buildSlogans(language, project, hooks, localizedIndustry, domain) {
  const name = domain || project || (language === "ar" ? "مشروعك" : "Your Project");
  const slogans = [];

  if (language === "ar") {
    slogans.push(
      `${name} أقرب ليك`,
      `محتوى يرافق يومك`,
      `استمع واستمتع`,
      `من الطريق إلى البيت`,
      `محتوى يفهم جمهورك`,
      `حضور أقرب ورسالة أوضح`,
      `محتوى أقرب للحياة`,
      `أفكار تسمعها وتعيشها`,
      `كل يوم قصة جديدة`,
      hooks[0] || `${localizedIndustry} بروح مختلفة`
    );
  } else {
    slogans.push(
      `${name}, closer to you`,
      `Content for your everyday life`,
      `Listen and enjoy`,
      `From the road to home`,
      `Content that understands your audience`,
      `Clearer message, stronger presence`,
      `Content closer to real life`,
      `Ideas you can hear and live`,
      `A new story every day`,
      hooks[0] || `${localizedIndustry} with a better angle`
    );
  }

  return uniqueList(slogans).slice(0, 10);
}

function buildCTAs(language, hooks, localizedIndustry) {
  const ctas = [];

  if (language === "ar") {
    ctas.push(
      "ابدأ الآن",
      "اكتشف أكثر",
      "جرّب اليوم",
      "شاهد المزيد",
      "استمع الآن",
      "ابدأ الاستماع",
      "استكشف المحتوى",
      "اكتشف التجربة",
      hooks[0] || `اكتشف ${localizedIndustry}`,
      `ابدأ مع ${localizedIndustry}`
    );
  } else {
    ctas.push(
      "Get Started",
      "Discover More",
      "Try It Today",
      "See More",
      "Listen Now",
      "Start Listening",
      "Explore Content",
      "Discover the Experience",
      hooks[0] || `Discover ${localizedIndustry}`,
      `Start with ${localizedIndustry}`
    );
  }

  return uniqueList(ctas).slice(0, 10);
}

function buildContentIdeas(language, seeds, audience, hooks, localizedIndustry) {
  const ideas = [];
  const topSeeds = seeds.slice(0, 6);

  if (language === "ar") {
    topSeeds.forEach(seed => ideas.push(`محتوى حول ${seed}`));

    if (hooks.some(h => h.includes("الطريق") || h.includes("المواصلات"))) {
      ideas.push("محتوى مناسب للطريق والمواصلات");
    }
    if (hooks.some(h => h.includes("البيت") || h.includes("المنزل"))) {
      ideas.push("محتوى يناسب ربات المنزل وأوقات البيت");
    }
    if (hooks.some(h => h.includes("الكبار"))) {
      ideas.push("محتوى سهل ومريح للكبار");
    }

    ideas.push(
      `أفكار محتوى في ${localizedIndustry}`,
      "مواضيع قريبة من اهتمامات الجمهور",
      "محتوى بسيط سهل الاستهلاك",
      "مواضيع قابلة للمشاركة",
      audience ? `محتوى مبني على احتياجات ${audience}` : "محتوى مبني على وصف الجمهور"
    );
  } else {
    topSeeds.forEach(seed => ideas.push(`Content around ${seed}`));

    if (hooks.some(h => h.toLowerCase().includes("road") || h.toLowerCase().includes("commute"))) {
      ideas.push("Content designed for the commute");
    }
    if (hooks.some(h => h.toLowerCase().includes("home"))) {
      ideas.push("Content that fits home routines");
    }
    if (hooks.some(h => h.toLowerCase().includes("older"))) {
      ideas.push("Comfortable content for older audiences");
    }

    ideas.push(
      `${localizedIndustry} content ideas`,
      "Topics close to audience interests",
      "Simple, easy-to-consume content",
      "Shareable content themes",
      audience ? `Content built around ${audience}` : "Content built around audience description"
    );
  }

  return uniqueList(ideas).slice(0, 10);
}

function generateResults() {
  showLoader();

  setTimeout(() => {
    const language = document.getElementById("language").value;
    const project = document.getElementById("projectName").value.trim();
    const url = document.getElementById("url").value.trim();
    const domain = extractDomain(url);
    const platformType = document.getElementById("platformType").value.trim();
    const service = document.getElementById("service").value.trim();
    const location = document.getElementById("location").value.trim();
    const industry = document.getElementById("industry").value.trim();
    const audience = document.getElementById("audience").value.trim();
    const seedText = document.getElementById("seedKeywords").value.trim();
    const seeds = parseSeedKeywords(seedText);

    updateDirection(language);

    const localizedIndustry = localizeIndustry(industry, language);
    const platformLabel = localizePlatform(platformType, language);
    const audienceSignals = detectAudienceSignals(audience, language);
    const audienceHooks = buildAudienceHooks(audienceSignals, language);

    const brandMessage = buildBrandMessage(
      language,
      project,
      platformLabel,
      localizedIndustry,
      audience,
      audienceHooks,
      domain
    );

    const seoTitle = buildSeoTitle(language, project, localizedIndustry, seeds, domain);
    const metaDescription = buildMetaDescription(
      language,
      project,
      localizedIndustry,
      audience,
      audienceHooks,
      seeds,
      location,
      domain
    );

    const seoKeywords = makeSeoKeywords(
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

    const shortHeadlines = buildShortHeadlines(
      language,
      project,
      localizedIndustry,
      audienceHooks,
      seeds,
      domain,
      audience
    );

    const longHeadlines = buildLongHeadlines(
      language,
      project,
      localizedIndustry,
      audienceHooks,
      seeds,
      domain,
      location
    );

    const descriptions = buildDescriptions(
      language,
      project,
      localizedIndustry,
      audienceHooks,
      seeds,
      audience,
      domain
    );

    const slogans = buildSlogans(
      language,
      project,
      audienceHooks,
      localizedIndustry,
      domain
    );

    const ctas = buildCTAs(language, audienceHooks, localizedIndustry);
    const contentIdeas = buildContentIdeas(language, seeds, audience, audienceHooks, localizedIndustry);

    document.getElementById("statProject").textContent = project || "—";
    document.getElementById("statIndustry").textContent = localizedIndustry || "—";
    document.getElementById("statLocation").textContent = location || "—";

    document.getElementById("brandMessage").innerHTML = brandMessage
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    document.getElementById("seoTitle").innerHTML = `<div class="result-item">${seoTitle}</div>`;
    document.getElementById("metaDescription").innerHTML = `<div class="result-item">${metaDescription}</div>`;

    document.getElementById("primaryKeywords").innerHTML = seoKeywords.primary
      .map(item => `<span class="keyword">${item}</span>`)
      .join("");

    document.getElementById("supportingKeywords").innerHTML = seoKeywords.supporting
      .map(item => `<span class="keyword">${item}</span>`)
      .join("");

    document.getElementById("slogans").innerHTML = slogans
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    document.getElementById("shortHeadlines").innerHTML = shortHeadlines
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    document.getElementById("longHeadlines").innerHTML = longHeadlines
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    document.getElementById("descriptions").innerHTML = descriptions
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    document.getElementById("ctaButtons").innerHTML = ctas
      .map(item => `<span class="cta">${item}</span>`)
      .join("");

    document.getElementById("contentIdeas").innerHTML = contentIdeas
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    hideLoader();
  }, 500);
}

function resetResults() {
  document.getElementById("language").value = "en";
  document.getElementById("projectName").value = "";
  document.getElementById("url").value = "";
  document.getElementById("platformType").value = "";
  document.getElementById("service").value = "";
  document.getElementById("location").value = "";
  document.getElementById("industry").value = "";
  document.getElementById("audience").value = "";
  document.getElementById("seedKeywords").value = "";

  updateDirection("en");

  document.getElementById("statProject").textContent = "—";
  document.getElementById("statIndustry").textContent = "—";
  document.getElementById("statLocation").textContent = "—";

  document.getElementById("brandMessage").innerHTML = `<div class="empty">No brand message yet.</div>`;
  document.getElementById("seoTitle").innerHTML = `<div class="empty">No SEO title yet.</div>`;
  document.getElementById("metaDescription").innerHTML = `<div class="empty">No meta description yet.</div>`;
  document.getElementById("primaryKeywords").innerHTML = `<div class="empty">No keywords yet.</div>`;
  document.getElementById("supportingKeywords").innerHTML = `<div class="empty">No supporting keywords yet.</div>`;
  document.getElementById("slogans").innerHTML = `<div class="empty">No slogans yet.</div>`;
  document.getElementById("shortHeadlines").innerHTML = `<div class="empty">No short headlines yet.</div>`;
  document.getElementById("longHeadlines").innerHTML = `<div class="empty">No long headlines yet.</div>`;
  document.getElementById("descriptions").innerHTML = `<div class="empty">No descriptions yet.</div>`;
  document.getElementById("ctaButtons").innerHTML = `<div class="empty">No CTA suggestions yet.</div>`;
  document.getElementById("contentIdeas").innerHTML = `<div class="empty">No content ideas yet.</div>`;
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

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

function makeSmartKeywords(service, industry, audience, location, language, domain, platformType) {
  const s = service || (language === "ar" ? "الخدمة" : "service");
  const i = industry || (language === "ar" ? "المجال" : "industry");
  const a = audience || (language === "ar" ? "الجمهور" : "audience");
  const l = location || "";
  const p = platformType || (language === "ar" ? "منصة" : "platform");
  const base = domain || s;

  if (language === "ar") {
    return {
      primary: [
        `${base}`,
        `${i}`,
        `${p} ${i}`,
        `${s} لـ ${a}`,
        l ? `${i} في ${l}` : `أفضل ${i}`,
        `${s} ${i}`
      ],
      lsi: [
        `حلول ${i}`,
        `كلمات مفتاحية ${i}`,
        `استهداف ${a}`,
        `زيادة الظهور الرقمي`,
        `تحسين محركات البحث`,
        `نمو العلامة التجارية`,
        `الوصول للعملاء`,
        l ? `${i} ${l}` : `تسويق ${i}`
      ]
    };
  }

  return {
    primary: [
      `${base}`,
      `${industry}`,
      `${platformType} ${industry}`,
      `${service} for ${audience}`,
      location ? `${industry} in ${location}` : `best ${industry}`,
      `${service} ${industry}`
    ],
    lsi: [
      `${industry} solutions`,
      `${industry} keywords`,
      `targeting ${audience}`,
      `digital visibility`,
      `search engine optimization`,
      `brand growth`,
      `customer reach`,
      location ? `${industry} ${location}` : `${industry} marketing`
    ]
  };
}

function makeAdCopy(project, service, industry, audience, location, language, domain, platformType) {
  const baseName = domain || project;

  if (language === "ar") {
    return {
      shortHeadlines: [
        domain ? `اكتشف ${domain}` : `طوّر ${project}`,
        `${industry} بطريقة أذكى`,
        `حلول ${service} لـ ${audience}`,
        location ? `وسع وصولك في ${location}` : `${platformType} يخدم جمهورك`
      ],
      longHeadlines: [
        `${baseName} يقدم حلول ${industry} بشكل أكثر ذكاءً وفعالية.`,
        `${service} يساعد ${audience} على الوصول إلى نتائج أفضل ونمو أسرع.`,
        location
          ? `طوّر حضورك في ${location} مع ${platformType} متخصص في ${industry}.`
          : `امنح جمهورك تجربة أفضل مع ${platformType} متخصص في ${industry}.`
      ],
      ctas: [
        "ابدأ الآن",
        "اكتشف المزيد",
        "جرّب اليوم",
        "تواصل معنا"
      ]
    };
  }

  return {
    shortHeadlines: [
      domain ? `Discover ${domain}` : `Boost ${project}`,
      `${industry} made smarter`,
      `${service} for ${audience}`,
      location ? `Grow faster in ${location}` : `${platformType} built for your audience`
    ],
    longHeadlines: [
      `${baseName} delivers smarter ${industry} solutions for better growth.`,
      `${service} helps ${audience} attract more attention and stronger results.`,
      location
        ? `Build a stronger presence in ${location} with a ${platformType} focused on ${industry}.`
        : `Give your audience a better experience with a ${platformType} built for ${industry}.`
    ],
    ctas: [
      "Get Started",
      "Discover More",
      "Try It Today",
      "Contact Us"
    ]
  };
}

function makeContentIdeas(industry, language) {
  const ideas = {
    en: {
      "Food / Cooking": [
        "5 easy recipes anyone can make at home",
        "Quick dinner ideas for busy weekdays",
        "Healthy breakfast ideas to start the day",
        "Common cooking mistakes and how to avoid them"
      ],
      "Podcast / Storytelling": [
        "Short story episode ideas for weekly publishing",
        "Emotional storytelling topics that attract listeners",
        "How to turn daily moments into podcast stories",
        "Story series ideas that keep the audience waiting"
      ],
      "Audiobooks / Books": [
        "Top audiobook categories listeners love most",
        "Book summary ideas for busy audiences",
        "How audiobooks fit into daily routines",
        "Arabic listening content ideas for knowledge seekers"
      ],
      "Sports": [
        "Weekly football analysis ideas for fans",
        "Match-day content ideas that drive engagement",
        "Player spotlight topics for sports audiences",
        "Quick sports facts people love to share"
      ],
      "Health / Wellness": [
        "Simple daily wellness habits to share",
        "Healthy lifestyle tips for beginners",
        "Stress relief content ideas for modern audiences",
        "Practical health awareness topics with strong appeal"
      ],
      "Beauty": [
        "Beginner beauty routine ideas",
        "Daily skincare tips that audiences love",
        "Common beauty mistakes and easy fixes",
        "Natural beauty habits worth sharing"
      ],
      "Kids": [
        "Short educational content ideas for children",
        "Fun learning activities for young minds",
        "Safe storytelling topics for kids",
        "Creative play ideas that support learning"
      ],
      "Education": [
        "Simple learning tips for students",
        "Study habit content ideas for better results",
        "Explainer content topics for complex subjects",
        "Skill-building ideas for everyday learners"
      ],
      "Technology": [
        "Beginner-friendly tech explainer ideas",
        "Simple tools that improve productivity",
        "Trending digital topics worth creating content about",
        "How-to content ideas for everyday technology users"
      ],
      "Retail": [
        "Seasonal product promotion ideas",
        "Content ideas that build shopping confidence",
        "How to highlight product benefits clearly",
        "Customer-focused retail storytelling ideas"
      ],
      "Finance": [
        "Simple money tips for everyday users",
        "Budgeting content ideas for beginners",
        "Financial awareness topics people search for",
        "Easy personal finance education ideas"
      ],
      "Travel": [
        "Travel planning tips for first-time visitors",
        "Destination guide ideas that attract clicks",
        "Budget travel content ideas",
        "Travel checklist topics for busy audiences"
      ]
    },
    ar: {
      "Food / Cooking": [
        "أفكار وصفات سهلة يمكن لأي شخص إعدادها في المنزل",
        "أفكار عشاء سريع لأيام الأسبوع المزدحمة",
        "أفكار فطور صحي لبداية يوم أفضل",
        "أخطاء طبخ شائعة وكيفية تجنبها"
      ],
      "Podcast / Storytelling": [
        "أفكار حلقات قصص قصيرة للنشر الأسبوعي",
        "مواضيع حكاوي مؤثرة تجذب المستمعين",
        "كيف تحوّل المواقف اليومية إلى قصص بودكاست",
        "أفكار سلاسل قصصية تشد الجمهور"
      ],
      "Audiobooks / Books": [
        "أكثر فئات الكتب المسموعة جذبًا للمستمعين",
        "أفكار ملخصات كتب للجمهور المشغول",
        "كيف تدخل الكتب المسموعة في الروتين اليومي",
        "أفكار محتوى سمعي عربي لعشاق المعرفة"
      ],
      "Sports": [
        "أفكار تحليل أسبوعي لمباريات كرة القدم",
        "أفكار محتوى يوم المباراة لزيادة التفاعل",
        "مواضيع تسليط الضوء على اللاعبين",
        "حقائق رياضية سريعة يحب الناس مشاركتها"
      ],
      "Health / Wellness": [
        "عادات يومية بسيطة للصحة والعافية",
        "نصائح نمط حياة صحي للمبتدئين",
        "أفكار محتوى لتخفيف التوتر",
        "مواضيع توعوية صحية ذات جاذبية قوية"
      ],
      "Beauty": [
        "أفكار روتين جمال للمبتدئات",
        "نصائح يومية للعناية بالبشرة",
        "أخطاء جمالية شائعة وحلولها السهلة",
        "عادات جمال طبيعية تستحق المشاركة"
      ],
      "Kids": [
        "أفكار محتوى تعليمي قصير للأطفال",
        "أنشطة ممتعة لتنمية عقول الصغار",
        "مواضيع حكايات آمنة للأطفال",
        "أفكار لعب إبداعية تدعم التعلم"
      ],
      "Education": [
        "نصائح تعلم بسيطة للطلاب",
        "أفكار محتوى لعادات دراسة أفضل",
        "مواضيع شرح مبسط للمواد المعقدة",
        "أفكار لبناء المهارات اليومية"
      ],
      "Technology": [
        "أفكار شرح تقني سهلة للمبتدئين",
        "أدوات بسيطة تحسن الإنتاجية",
        "مواضيع رقمية رائجة تستحق صناعة محتوى عنها",
        "أفكار محتوى تعليمي لاستخدام التكنولوجيا اليومية"
      ],
      "Retail": [
        "أفكار ترويج موسمية للمنتجات",
        "محتوى يساعد على زيادة ثقة المشتري",
        "كيف تبرز فوائد المنتج بشكل واضح",
        "أفكار قصص تسويقية تناسب قطاع التجزئة"
      ],
      "Finance": [
        "نصائح مالية بسيطة للحياة اليومية",
        "أفكار محتوى عن الميزانية للمبتدئين",
        "مواضيع توعية مالية يبحث عنها الناس",
        "أفكار سهلة للتثقيف المالي الشخصي"
      ],
      "Travel": [
        "نصائح تخطيط سفر للمبتدئين",
        "أفكار أدلة وجهات تجذب النقرات",
        "أفكار محتوى للسفر الاقتصادي",
        "مواضيع قوائم السفر للجمهور المشغول"
      ]
    }
  };

  const langKey = language === "ar" ? "ar" : "en";
  return ideas[langKey][industry] || (language === "ar"
    ? [
        "أفكار محتوى تعريفية بالمشروع",
        "مواضيع تجذب الجمهور المستهدف",
        "محتوى يبرز الفوائد الأساسية",
        "أفكار محتوى قابلة للمشاركة"
      ]
    : [
        "Project introduction content ideas",
        "Topics that attract the target audience",
        "Content highlighting key benefits",
        "Shareable content ideas for engagement"
      ]);
}

function generateResults() {
  showLoader();

  setTimeout(() => {
    const language = document.getElementById("language").value;
    const project =
      document.getElementById("projectName").value.trim() ||
      (language === "ar" ? "مشروعك" : "Your Project");
    const url = document.getElementById("url").value.trim();
    const domain = extractDomain(url);
    const platformType =
      document.getElementById("platformType").value.trim() ||
      (language === "ar" ? "منصة" : "platform");
    const service =
      document.getElementById("service").value.trim() ||
      (language === "ar" ? "خدمتك" : "your service");
    const location =
      document.getElementById("location").value.trim() ||
      (language === "ar" ? "سوقك" : "your market");
    const industry =
      document.getElementById("industry").value.trim() ||
      (language === "ar" ? "مجالك" : "your industry");
    const audience =
      document.getElementById("audience").value.trim() ||
      (language === "ar" ? "جمهورك" : "your audience");

    updateDirection(language);

    const ads = makeAdCopy(
      project,
      service,
      industry,
      audience,
      location,
      language,
      domain,
      platformType
    );

    const keywordsData = makeSmartKeywords(
      service,
      industry,
      audience,
      location,
      language,
      domain,
      platformType
    );

    const contentIdeas = makeContentIdeas(industry, language);

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

    document.getElementById("contentIdeas").innerHTML = contentIdeas
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    hideLoader();
  }, 900);
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
  document.getElementById("contentIdeas").innerHTML =
    `<div class="empty">No content ideas yet.</div>`;
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

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

function generateResults() {
  showLoader();

  setTimeout(() => {
    const project = document.getElementById("projectName").value.trim() || "Your Project";
    const service = document.getElementById("service").value.trim() || "your service";
    const location = document.getElementById("location").value.trim() || "your market";
    const industry = document.getElementById("industry").value.trim() || "your industry";
    const audience = document.getElementById("audience").value.trim() || "your audience";

    const shortHeadlines = [
      `Boost ${project}`,
      `Grow with ${service}`,
      `Reach more clients in ${location}`,
      `${industry} made simpler`
    ];

    const longHeadlines = [
      `Discover how ${service} helps ${audience} achieve faster growth.`,
      `Scale your ${industry} business in ${location} with smarter marketing.`,
      `${project} gives you a better way to attract, engage, and convert customers.`
    ];

    const keywords = [
      service,
      `${industry} solutions`,
      `best ${service}`,
      `${location} ${industry}`,
      `${audience} tools`
    ];

    const lsi = [
      "growth strategy",
      "customer acquisition",
      "digital visibility",
      "brand awareness",
      "lead generation"
    ];

    const ctas = [
      "Get Started",
      "Request Demo",
      "Contact Us",
      "Start Today"
    ];

    document.getElementById("statProject").textContent = project;
    document.getElementById("statIndustry").textContent = industry;
    document.getElementById("statLocation").textContent = location;

    document.getElementById("shortHeadlines").innerHTML = shortHeadlines
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    document.getElementById("longHeadlines").innerHTML = longHeadlines
      .map(item => `<div class="result-item">${item}</div>`)
      .join("");

    document.getElementById("primaryKeywords").innerHTML = keywords
      .map(item => `<span class="keyword">${item}</span>`)
      .join("");

    document.getElementById("lsiKeywords").innerHTML = lsi
      .map(item => `<span class="keyword">${item}</span>`)
      .join("");

    document.getElementById("ctaButtons").innerHTML = ctas
      .map(item => `<span class="cta">${item}</span>`)
      .join("");

    hideLoader();
  }, 900);
}

function resetResults() {
  document.getElementById("projectName").value = "";
  document.getElementById("service").value = "";
  document.getElementById("location").value = "";
  document.getElementById("industry").value = "";
  document.getElementById("audience").value = "";

  document.getElementById("statProject").textContent = "—";
  document.getElementById("statIndustry").textContent = "—";
  document.getElementById("statLocation").textContent = "—";

  document.getElementById("shortHeadlines").innerHTML = `<div class="empty">No headlines yet.</div>`;
  document.getElementById("longHeadlines").innerHTML = `<div class="empty">No long headlines yet.</div>`;
  document.getElementById("primaryKeywords").innerHTML = `<div class="empty">No keywords yet.</div>`;
  document.getElementById("lsiKeywords").innerHTML = `<div class="empty">No LSI keywords yet.</div>`;
  document.getElementById("ctaButtons").innerHTML = `<div class="empty">No CTA suggestions yet.</div>`;
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

const form = document.querySelector("#research-form");
const question = document.querySelector("#question");
const answer = document.querySelector("#answer");
const button = document.querySelector("#submit-button");
const charCount = document.querySelector("#char-count");
const agentCards = [...document.querySelectorAll(".agent-card")];

question.addEventListener("input", () => {
  charCount.textContent = `${question.value.length} / 2000`;
  question.style.height = "auto";
  question.style.height = `${question.scrollHeight}px`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const value = question.value.trim();
  if (!value) return;

  button.disabled = true;
  button.querySelector("span").textContent = "Researching...";
  setResearchState("running");
  answer.innerHTML = '<div class="answer-placeholder"><p>Agents are researching your question...</p></div>';

  try {
    const response = await fetch("/api/research", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: value }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "The request could not be completed.");
    renderReport(data);
    setResearchState("complete");
  } catch (error) {
    answer.innerHTML = `<div class="answer-placeholder"><p class="error">${escapeHtml(error.message)}</p></div>`;
    setResearchState("error");
  } finally {
    button.disabled = false;
    button.querySelector("span").textContent = "Start research";
  }
});

function renderReport(plan) {
  const result = plan.plan ? plan : { plan };
  const researchPlan = result.plan || {};
  const review = result.review || { confidence_assessment: "unknown", summary: "No review was returned." };
  const sources = result.sources || [];
  const answerText = result.answer || "The research plan was created, but no synthesized answer was returned.";
  const evidence = result.evidence || [];
  const gaps = review.gaps || [];

  answer.innerHTML = `
    <span class="meta">Final research report</span>
    <h2>${escapeHtml(researchPlan.question)}</h2>
    <section class="report-block report-conclusion"><h3>Conclusion</h3><p class="answer-copy">${escapeHtml(answerText).replace(/\n+/g, "<br><br>")}</p></section>
    <section class="report-block"><h3>Research plan</h3><p>${escapeHtml(researchPlan.research_strategy || "")}</p><ul>${(researchPlan.subquestions || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></section>
    <section class="report-block critic-block"><h3>Critic review</h3><p><strong>${escapeHtml(review.confidence_assessment || "unknown").toUpperCase()}</strong> confidence. ${escapeHtml(review.summary || "")}</p><p class="gap-label">${gaps.length ? "Evidence gaps detected - additional research required" : "No critical evidence gaps detected"}</p>${gaps.length ? `<ul>${gaps.map((gap) => `<li>${escapeHtml(gap)}</li>`).join("")}</ul>` : ""}</section>
    <section class="report-block"><h3>Evidence reviewed</h3><ul>${evidence.map((item) => `<li>${escapeHtml(item.claim)} <span class="confidence">[${escapeHtml(item.confidence)}]</span></li>`).join("")}</ul><h3>Sources</h3><ul>${sources.map((source) => `<li><a href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(source.title)}</a></li>`).join("")}</ul></section>`;
}

function setResearchState(state) {
  agentCards.forEach((card) => card.classList.remove("is-active", "is-complete", "is-error"));
  if (state === "running") {
    agentCards.forEach((card, index) => setTimeout(() => card.classList.add("is-active"), index * 180));
  }
  if (state === "complete") agentCards.forEach((card) => card.classList.add("is-complete"));
  if (state === "error") agentCards.forEach((card) => card.classList.add("is-error"));
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;",
  }[character]));
}
async function loadSearchDocuments(form) {
  if (window.searchDocuments) {
    return window.searchDocuments;
  }

  const response = await fetch(form.dataset.searchUrl);
  const data = await response.json();
  window.searchDocuments = data.documents || [];
  return window.searchDocuments;
}

function renderResults(resultsElement, documents, query) {
  resultsElement.innerHTML = "";

  if (!query) {
    return;
  }

  const normalizedQuery = query.toLowerCase();
  const matches = documents.filter((entry) => {
    const haystack = [
      entry.title,
      entry.content,
      (entry.tags || []).join(" "),
    ].join(" ").toLowerCase();
    return haystack.includes(normalizedQuery);
  });

  matches.forEach((entry) => {
    const item = window.document.createElement("li");
    const link = window.document.createElement("a");
    link.href = entry.url;
    link.textContent = entry.title;
    item.appendChild(link);
    resultsElement.appendChild(item);
  });

  if (!matches.length) {
    const item = window.document.createElement("li");
    item.textContent = "No results found.";
    resultsElement.appendChild(item);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#search");
  const input = document.querySelector("#search-input");
  const results = document.querySelector("#results");

  if (form && input && results) {
    const params = new URLSearchParams(window.location.search);
    input.value = params.get("query") || "";

    loadSearchDocuments(form).then((documents) => {
      renderResults(results, documents, input.value.trim());
    });

    input.addEventListener("input", async () => {
      const documents = await loadSearchDocuments(form);
      renderResults(results, documents, input.value.trim());
    });

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      renderResults(results, window.searchDocuments || [], input.value.trim());
    });
  }

  document.addEventListener("keydown", (event) => {
    const active = document.activeElement;
    if (active && (active.isContentEditable || ["INPUT", "TEXTAREA"].includes(active.tagName))) {
      return;
    }
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) {
      return;
    }
    if (event.key === "h") {
      event.preventDefault();
      window.location.href = "/";
    }
    if (event.key === "i" && input) {
      event.preventDefault();
      input.focus();
      input.setSelectionRange(input.value.length, input.value.length);
    }
  });
});

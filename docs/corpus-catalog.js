(() => {
  "use strict";
  const tools = document.getElementById("catalogueTools");
  const search = document.getElementById("catalogueSearch");
  const filter = document.getElementById("interpretationFilter");
  const status = document.getElementById("catalogueStatus");
  const empty = document.getElementById("catalogueEmpty");
  const cards = Array.from(document.querySelectorAll(".catalogue-card"));
  const normalize = value => value.normalize("NFD").replace(/\p{M}/gu, "").toLocaleLowerCase("es").trim();
  const texts = new Map(cards.map(card => [card.id, normalize(card.textContent)]));
  function applyFilters() {
    const term = normalize(search.value);
    let visible = 0;
    for (const card of cards) {
      const semantic = card.dataset.semantic;
      const interpretationMatch = filter.value === "all" || filter.value === semantic ||
        (filter.value === "identified" && ["identified_name", "identified_referent"].includes(semantic));
      card.hidden = !interpretationMatch || !texts.get(card.id).includes(term);
      if (!card.hidden) visible += 1;
    }
    status.textContent = `${visible} de ${cards.length} fichas disponibles.`;
    empty.hidden = visible > 0;
  }
  function reset() {
    search.value = "";
    filter.value = "all";
    applyFilters();
  }
  function revealFragment(fragment) {
    const card = cards.find(item => `#${item.id}` === fragment);
    if (card?.hidden) {
      reset();
      card.scrollIntoView({ block: "start" });
    }
  }
  search.addEventListener("input", applyFilters);
  filter.addEventListener("change", applyFilters);
  tools.addEventListener("submit", event => { event.preventDefault(); applyFilters(); });
  document.getElementById("clearCatalogueFilters").addEventListener("click", reset);
  document.querySelectorAll('.catalogue-index a').forEach(link => {
    link.addEventListener("click", () => revealFragment(link.hash));
  });
  window.addEventListener("hashchange", () => revealFragment(location.hash));
  tools.hidden = false;
  applyFilters();
})();

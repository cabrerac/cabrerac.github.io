document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-content-tabs]").forEach((root) => {
    const tabs = [...root.querySelectorAll(".content-tab")];
    const panels = [...root.querySelectorAll(".content-tabpanel")];
    if (tabs.length === 0) return;

    function activate(tabId, updateHash) {
      tabs.forEach((tab) => {
        const active = tab.dataset.tab === tabId;
        tab.classList.toggle("is-active", active);
        tab.setAttribute("aria-selected", active ? "true" : "false");
      });
      panels.forEach((panel) => {
        const active = panel.dataset.panel === tabId;
        panel.classList.toggle("is-active", active);
        panel.hidden = !active;
      });
      if (updateHash && tabId) {
        const url = `${window.location.pathname}${window.location.search}#${tabId}`;
        window.history.replaceState(null, "", url);
      }
    }

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => activate(tab.dataset.tab, true));
    });

    const hash = window.location.hash.slice(1);
    if (hash && tabs.some((tab) => tab.dataset.tab === hash)) {
      activate(hash, false);
    }
  });
});

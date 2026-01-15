(() => {
  const script = document.currentScript;
  const gaId = script?.dataset?.gaId;

  if (!gaId) {
    return;
  }

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }

  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", gaId);
})();

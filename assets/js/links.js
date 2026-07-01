(() => {
  const TEACHING_PATH = /^\/teaching\//;
  const NEW_TAB_ASSET_PATH = /^\/assets\/(?:slides|notebooks|docs)\//;
  const SAME_TAB_DOCUMENT_PATH = /^\/assets\/documents\//;
  const SAME_TAB_DOCUMENT_EXT = /\.(docx|pptx|txt)$/i;

  function resolveUrl(href) {
    try {
      return new URL(href, window.location.href);
    } catch {
      return null;
    }
  }

  function shouldOpenNewTab(anchor) {
    if (anchor.dataset.linkScope === 'same-tab') return false;
    if (anchor.dataset.linkScope === 'new-tab') return true;
    if (anchor.classList.contains('course-nav__internal')) return false;

    const href = anchor.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) {
      return false;
    }

    const url = resolveUrl(href);
    if (!url) return false;

    const sameOrigin = url.origin === window.location.origin;
    const path = url.pathname;

    if (sameOrigin && TEACHING_PATH.test(path)) {
      return false;
    }

    if (sameOrigin && SAME_TAB_DOCUMENT_PATH.test(path) && SAME_TAB_DOCUMENT_EXT.test(path)) {
      return false;
    }

    if (sameOrigin && /\.pdf$/i.test(path)) {
      return true;
    }

    if (sameOrigin && NEW_TAB_ASSET_PATH.test(path)) {
      return true;
    }

    return !sameOrigin;
  }

  function applyLinkPolicy(root) {
    root.querySelectorAll('a[href]').forEach((anchor) => {
      if (shouldOpenNewTab(anchor)) {
        anchor.target = '_blank';
        anchor.rel = 'noopener noreferrer';
        return;
      }

      anchor.removeAttribute('target');
      anchor.removeAttribute('rel');
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    const main = document.querySelector('main');
    if (main) applyLinkPolicy(main);
  });
})();

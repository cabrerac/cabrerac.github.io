// Add theme toggle button to body once slides load
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.createElement("div");
  toggle.id = "theme-toggle";
  toggle.innerHTML = "🌔";
  document.body.appendChild(toggle);

  const style = document.createElement("style");
  style.textContent = `
    #theme-toggle {
      position: fixed;
      top: 1rem;
      right: 1rem;
      background: var(--accent-color);
      color: var(--background-color);
      padding: 0.5em;
      width: 1.5em;
      height: 1.5em;
      border-radius: 50%;
      font-size: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 9999;
      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
      user-select: none;
      transition: transform 0.3s ease;
    }
    
    #theme-toggle:hover {
      transform: scale(1.1);
    }
    
    html[data-theme='dark'] {
      --primary-color: #FFFFFF;
      --secondary-color: #0E73B8;
      --accent-color: #0E73B8;
      --text-color: #FFFFFF;
      --background-color: #1E1E1E;
      --progress-color: #0E73B8;
    }
    
    html[data-theme='light'] {
      --primary-color: #00244A;
      --secondary-color: #0E73B8;
      --accent-color: #0E73B8;
      --text-color: #00244A;
      --background-color: #FFFFFF;
      --progress-color: #0E73B8;
    }
    
    html[data-theme='dark'] section {
      background-color: #1E1E1E !important;
      color: #FFFFFF !important;
    }
    
    html[data-theme='dark'] h1, 
    html[data-theme='dark'] h2, 
    html[data-theme='dark'] h3, 
    html[data-theme='dark'] h4, 
    html[data-theme='dark'] h5, 
    html[data-theme='dark'] h6 {
      color: #FFFFFF !important;
    }
    
    html[data-theme='dark'] a {
      color: #0E73B8 !important;
    }
    
    html[data-theme='dark'] body,
    html[data-theme='dark'] .marpit {
      background-color: #1E1E1E !important;
    }
    
    html[data-theme='dark'] header {
      color: #FFFFFF !important;
    }

    /* Explicit dark mode styles for paragraphs and their children */
    html[data-theme='dark'] section p,
    html[data-theme='dark'] section p *,
    html[data-theme='dark'] section .column p,
    html[data-theme='dark'] section .column p *,
    html[data-theme='dark'] section .row p,
    html[data-theme='dark'] section .row p *,
    html[data-theme='dark'] section p strong,
    html[data-theme='dark'] section p em,
    html[data-theme='dark'] section .column p strong,
    html[data-theme='dark'] section .column p em,
    html[data-theme='dark'] section .row p strong,
    html[data-theme='dark'] section .row p em {
      color: #FFFFFF !important;
    }
                  
    html[data-theme='dark'] section .pre {
      background-color: #2A2A2A !important;
    }

    /* Link styling */
    a {
      color: var(--accent-color);
      text-decoration: none;
    }

    a:hover {
      text-decoration: underline;
    }

    /* Ensure links maintain accent color in dark mode */
    html[data-theme='dark'] a {
      color: var(--accent-color) !important;
    }

    /* Override any specific link colors */
    html[data-theme='dark'] section p a,
    html[data-theme='dark'] section .column p a,
    html[data-theme='dark'] section .row p a {
      color: var(--accent-color) !important;
    }

    /* Ensure email links maintain accent color */
    html[data-theme='dark'] section p a[href^="mailto:"] {
      color: var(--accent-color) !important;
    }
  `;
  document.head.appendChild(style);

  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    toggle.innerHTML = theme === "dark" ? "🌔" : "🌒";
    
    // Force update paragraph colors
    if (theme === "dark") {
      document.querySelectorAll('section p, section p *, section .column p, section .column p *, section .row p, section .row p *').forEach(el => {
        el.style.color = '#FFFFFF !important';
      });
    }
  }

  toggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "light";
    setTheme(current === "dark" ? "light" : "dark");
  });

  const stored = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  if (stored) {
    setTheme(stored);
  } else {
    setTheme(prefersDark ? "dark" : "light");
  }
});
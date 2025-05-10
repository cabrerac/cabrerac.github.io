// Marp JavaScript functionality
document.addEventListener('DOMContentLoaded', () => {
  // Initialize Marp slides
  const slides = document.querySelectorAll('section');
  let currentSlide = 0;

  // Add slide navigation
  const addNavigation = () => {
    const nav = document.createElement('nav');
    nav.className = 'marp-navigation';
    nav.innerHTML = `
      <button id="prev-slide" aria-label="Previous slide">←</button>
      <span id="slide-counter">1 / ${slides.length}</span>
      <button id="next-slide" aria-label="Next slide">→</button>
    `;
    document.body.appendChild(nav);

    // Add keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        goToSlide(currentSlide - 1);
      } else if (e.key === 'ArrowRight') {
        goToSlide(currentSlide + 1);
      }
    });

    // Add button event listeners
    document.getElementById('prev-slide').addEventListener('click', () => goToSlide(currentSlide - 1));
    document.getElementById('next-slide').addEventListener('click', () => goToSlide(currentSlide + 1));
  };

  // Go to specific slide
  const goToSlide = (index) => {
    if (index < 0) index = 0;
    if (index >= slides.length) index = slides.length - 1;

    slides[currentSlide].style.display = 'none';
    slides[index].style.display = 'flex';
    currentSlide = index;

    // Update slide counter
    document.getElementById('slide-counter').textContent = `${currentSlide + 1} / ${slides.length}`;

    // Update URL hash
    window.location.hash = `#${currentSlide + 1}`;
  };

  // Initialize slides
  const initializeSlides = () => {
    slides.forEach((slide, index) => {
      if (index !== 0) {
        slide.style.display = 'none';
      }
    });

    // Check URL hash for initial slide
    const hash = window.location.hash;
    if (hash) {
      const slideIndex = parseInt(hash.substring(1)) - 1;
      if (!isNaN(slideIndex) && slideIndex >= 0 && slideIndex < slides.length) {
        goToSlide(slideIndex);
      }
    }
  };

  // Add presenter mode
  const addPresenterMode = () => {
    const togglePresenter = document.createElement('button');
    togglePresenter.id = 'toggle-presenter';
    togglePresenter.textContent = 'Presenter Mode';
    togglePresenter.addEventListener('click', () => {
      document.body.classList.toggle('presenter-mode');
    });
    document.querySelector('.marp-navigation').appendChild(togglePresenter);
  };

  // Add theme toggle button to body once slides load
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

  // Initialize everything
  initializeSlides();
  addNavigation();
  addPresenterMode();
}); 
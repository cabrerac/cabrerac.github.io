document.addEventListener("DOMContentLoaded", () => {
  const style = document.createElement("style");
  style.textContent = `
    .collapsible-header {
      cursor: pointer;
      user-select: none;
      padding: 1rem;
      margin: 0.5rem 0;
      background-color: var(--border-color);
      border-radius: 5px;
      transition: background-color 0.3s ease;
    }

    .collapsible-header:hover {
      background-color: #d3d3d3;
    }

    .collapsible-header::before {
      content: "▶ ";
      display: inline-block;
      transition: transform 0.3s ease;
      margin-right: 0.5rem;
    }

    .collapsible-header.active::before {
      transform: rotate(90deg);
    }

    .collapsible-content {
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.3s ease-out;
    }

    .collapsible-content.expanded {
      max-height: 10000px;
      transition: max-height 0.5s ease-in;
    }
  `;
  document.head.appendChild(style);

  document.querySelectorAll('.collapsible-header').forEach(header => {
    header.addEventListener('click', () => {
      const content = header.nextElementSibling;
      const isActive = header.classList.contains('active');

      // If clicking to open, close all other collapsible sections on the page
      if (!isActive) {
        document.querySelectorAll('.collapsible-header').forEach(otherHeader => {
          if (otherHeader !== header) {
            const otherContent = otherHeader.nextElementSibling;
            otherHeader.classList.remove('active');
            otherContent.classList.remove('expanded');
          }
        });
      }

      header.classList.toggle('active');
      content.classList.toggle('expanded');
    });
  });
});

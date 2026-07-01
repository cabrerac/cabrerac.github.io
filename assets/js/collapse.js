document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.collapsible-header').forEach(header => {
    header.addEventListener('click', () => {
      const content = header.nextElementSibling;
      const isActive = header.classList.contains('active');

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

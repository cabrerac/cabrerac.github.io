document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".collapsible-header").forEach((header) => {
    header.addEventListener("click", () => {
      const content = header.nextElementSibling;
      if (!content || !content.classList.contains("collapsible-content")) {
        return;
      }
      header.classList.toggle("active");
      content.classList.toggle("expanded");
    });
  });
});

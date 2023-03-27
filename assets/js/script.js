document.addEventListener('DOMContentLoaded', () => {
  const menuButton = document.getElementById('toggle-menu');
  const menu = document.querySelector('nav');

  menuButton.addEventListener('click', () => {
    menu.classList.toggle('menu-open');
  });
});
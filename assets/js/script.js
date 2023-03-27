const menuButton = document.getElementById('toggle-menu');
const menu = document.querySelector('nav ul');

menuButton.addEventListener('click', () => {
  menu.classList.toggle('menu-open');
});

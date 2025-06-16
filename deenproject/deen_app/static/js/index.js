const showMenu = (toggleId, navId) => {
  const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId),
        hero = document.getElementById('hero'),
        navBurger = document.getElementById('nav_burger'),
        navClose = document.getElementById('nav_close');

  if (toggle && nav) {
      toggle.addEventListener('click', () => {
          // Toggle the visibility of the menu
          nav.classList.toggle('show-menu');
          
          // Toggle between burger and close icons
          navBurger.classList.toggle('hide-icon');
          navClose.classList.toggle('show-icon');
          
          // Adjust hero section visibility when menu is toggled
          if (nav.classList.contains('show-menu')) {
              hero.style.opacity = '0.3';  // Make hero section less visible
          } else {
              hero.style.opacity = '1';    // Reset hero section to full visibility
          }
      });
  }
};

showMenu('nav-toggle', 'nav-menu');

document.getElementById('search_field').removeAttribute('autofocus');

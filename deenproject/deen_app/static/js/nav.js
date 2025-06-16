/*=============== SHOW MENU ===============*/

/*=============== SHOW MENU ===============*/
const showMenu = (toggleId, navId) =>{
  const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId)

  toggle.addEventListener('click', () =>{
      // Add show-menu class to nav menu
      nav.classList.toggle('show-menu')
      // Add show-icon to show and hide menu icon
      toggle.classList.toggle('show-icon')
  })
}

showMenu('nav-toggle','nav-menu')

/*=============== DARK MODE TOGGLE ===============*/
const darkModeToggle = document.getElementById('dark-mode-toggle');
const darkModeIcon = document.getElementById('dark-mode-icon');
const htmlElement = document.documentElement;

darkModeToggle.addEventListener('click', () => {
  htmlElement.classList.toggle('dark-mode');
  if (htmlElement.classList.contains('dark-mode')) {
    darkModeIcon.classList.replace('ri-moon-line', 'ri-sun-line');
  } else {
    darkModeIcon.classList.replace('ri-sun-line', 'ri-moon-line');
  }
});


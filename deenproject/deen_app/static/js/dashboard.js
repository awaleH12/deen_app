// Sidebar toggle
const sidebar = document.querySelector('.sidebar');
const sidebarToggle = document.querySelector('.sidebar-toggle');
const mainContent = document.querySelector('.main-content');

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('expanded');
    // For accessibility: update aria-expanded
    sidebarToggle.setAttribute('aria-expanded', sidebar.classList.contains('expanded'));
});

// Dark mode toggle
const darkModeToggle = document.querySelector('.dark-mode-toggle');
const htmlEl = document.documentElement;

function setDarkMode(on) {
    if (on) {
        htmlEl.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'on');
        darkModeToggle.innerHTML = '<i class="bx bx-sun"></i>';
    } else {
        htmlEl.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'off');
        darkModeToggle.innerHTML = '<i class="bx bx-moon"></i>';
    }
}

darkModeToggle.addEventListener('click', () => {
    setDarkMode(!htmlEl.classList.contains('dark-mode'));
});

// On load, set dark mode from localStorage
if (localStorage.getItem('darkMode') === 'on') {
    setDarkMode(true);
} else {
    setDarkMode(false);
}

// Profile dropdown
const profile = document.querySelector('.profile');
const profileDropdown = document.querySelector('.profile-dropdown');

profile.addEventListener('click', (e) => {
    e.stopPropagation();
    profile.classList.toggle('open');
});

// Close dropdown on outside click
document.addEventListener('click', (e) => {
    if (!profile.contains(e.target)) {
        profile.classList.remove('open');
    }
});

// Keyboard accessibility for profile dropdown
profile.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        profile.classList.toggle('open');
    }
});
'use strict';
const root = document.documentElement;
const toggle = document.getElementById('theme-toggle');
const savedTheme = (() => { try { return localStorage.getItem('learning-lab-theme'); } catch { return null; } })();
if (savedTheme === 'light' || savedTheme === 'dark') root.dataset.theme = savedTheme;
function refreshThemeButton() {
  toggle.textContent = root.dataset.theme === 'dark' ? '\u263e' : '\u2600';
  toggle.setAttribute('aria-label', root.dataset.theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
}
refreshThemeButton();
toggle.addEventListener('click', () => {
  root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem('learning-lab-theme',root.dataset.theme); } catch {}
  refreshThemeButton();
});
const input = document.getElementById('resource-search');
const chips = [...document.querySelectorAll('[data-filter]')];
const cards = [...document.querySelectorAll('.resource-card')];
const groups = [...document.querySelectorAll('[data-category-group]')];
const counter = document.getElementById('resource-counter');
const empty = document.getElementById('empty-resources');
let category = 'all';
function updateResources() {
  const q = input.value.trim().toLocaleLowerCase();
  let visibleCount = 0;
  cards.forEach(card => {
    const matches = (category === 'all' || card.dataset.category === category) && (!q || card.dataset.search.includes(q));
    card.hidden = !matches;
    if (matches) visibleCount++;
  });
  groups.forEach(group => { group.hidden = !group.querySelector('.resource-card:not([hidden])'); });
  counter.textContent = `${visibleCount} resource${visibleCount === 1 ? '' : 's'}`;
  empty.hidden = visibleCount !== 0;
}
chips.forEach(chip => chip.addEventListener('click', () => {
  category = chip.dataset.filter;
  chips.forEach(c => { const active = c === chip; c.classList.toggle('is-active', active); c.setAttribute('aria-pressed', String(active)); });
  updateResources();
}));
input.addEventListener('input', updateResources);

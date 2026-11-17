'use strict';
const root = document.documentElement;
const toggle = document.getElementById('theme-toggle');
const savedTheme = (() => { try { return localStorage.getItem('learning-lab-theme'); } catch { return null; } })();
root.dataset.theme = savedTheme === 'light' ? 'light' : 'dark';
function refreshThemeButton() {
  const dark = root.dataset.theme === 'dark';
  toggle.querySelector('.theme-symbol').textContent = dark ? '\u263e' : '\u2600';
  toggle.querySelector('.theme-label').textContent = dark ? 'Dark' : 'Light';
  toggle.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
  toggle.setAttribute('title', dark ? 'Switch to light theme' : 'Switch to dark theme');
  toggle.setAttribute('aria-pressed', String(dark));
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

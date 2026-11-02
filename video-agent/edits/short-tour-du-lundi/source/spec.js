// Short muet (papier seul) pour Traceo, menu du 02/11/2026, script s01 « Ton tour du lundi » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : l'ordre négatif (#2 Negative Command).
// Beats : 0 accroche (stop au tour du lundi) · 3.0 carte : le coureur tourne autour du même parc (même parc, même feu rouge, même virage)
// · 6.0 la boucle de 7 km sort, tracée en 10 s · 10.0 par des rues neuves + lien en bio.
// Identité propre : papier lilas #ECE8F3, encre #1E1A2E, accent violet #6A4FC2, DM Sans 800, lit « sonar ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Stop au tour du lundi : ta boucle de 7 km sort en 10 secondes.',
  silent: true, duration: 13,
  media: { carte: { src: 'assets/carte-lundi.mp4', width: 900 } },
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [
    { id: 'carte', media: 'carte', offset: 0, from: 3.0, to: 9.95, pre: 0, ar: 1, keys: [[3.0, [90, 300, 760]]] },
  ],
  scenes: [
    { type: 'board', from: 0, to: 2.95, items: [
      { k: 'chip', text: 'Lundi, 19 h', size: 50, x: 540, y: 650, at: 0, shown: true },
      { k: 'text', text: 'Stop', emph: 'Stop', emphAt: 0.3, size: 230, x: 540, y: 860, at: 0, shown: true },
      { k: 'text', text: 'au tour', size: 130, x: 540, y: 1050, at: 0, shown: true },
      { k: 'text', text: 'du lundi.', emph: 'lundi.', emphAt: 0.9, size: 130, x: 540, y: 1190, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.0, to: 5.95, items: [
      { k: 'text', text: 'Même parc, même feu rouge,', size: 66, x: 540, y: 1180, at: 3.2 },
      { k: 'text', text: 'même virage.', emph: 'même virage.', emphAt: 4.6, size: 104, x: 540, y: 1300, at: 3.8 },
    ] },
    { type: 'board', from: 6.0, to: 9.95, items: [
      { k: 'text', text: 'Ta boucle de 7 km', emph: '7 km', emphAt: 6.5, size: 90, x: 540, y: 1180, at: 6.05 },
      { k: 'text', text: 'sort en 10 secondes.', emph: '10 secondes.', emphAt: 8.6, size: 84, x: 540, y: 1300, at: 6.6 },
    ] },
    { type: 'board', from: 10.0, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 10.05 },
      { k: 'text', text: 'Par des', size: 120, x: 540, y: 850, at: 10.2 },
      { k: 'text', text: 'rues neuves.', emph: 'rues neuves.', emphAt: 10.8, size: 120, x: 540, y: 985, at: 10.45 },
      { k: 'check', s: 100, x: 540, y: 1130, at: 10.9 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 11.5, size: 96, x: 540, y: 1280, at: 11.2 },
    ] },
  ],
  music: { bed: 'sonar', offset: 8 },
  sfx: { swish: 0, accents: 0, extra: [[0.3, 'thud', -6], [3.25, 'pop', -7], [6.4, 'pop', -7], [8.9, 'thud', -7], [10.1, 'pop', -6], [11.2, 'thud', -5]] },
};

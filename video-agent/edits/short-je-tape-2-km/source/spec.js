// Short muet (papier seul) pour Traceo, menu du 31/10/2026, script s01 « Je tape 2 km » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : la démo à froid (#18 Cold Open Demo).
// Beats : 0 accroche (je tape 2 km, regarde la plus petite boucle sortir) · 3.0 carte : la boucle sort
// · 6.5 depuis ta porte, retour à ta porte (le coureur suit la boucle) · 10.1 la plus petite + lien en bio, écho « 2 km » (boucle).
// Identité propre : papier rosé #F3E6E1, encre brun #2B1D1A, accent #1C7DB0, TeX Gyre Heros Cn, lit « labo ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Je tape 2 km. Regarde la plus petite boucle sortir.',
  silent: true, duration: 13,
  media: { carte: { src: 'assets/carte-2km.mp4', width: 900 } },
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [
    { id: 'carte', media: 'carte', offset: 0, from: 3.0, to: 10.0, pre: 0, ar: 1, keys: [[3.0, [160, 300, 760]]] },
  ],
  scenes: [
    { type: 'board', from: 0, to: 2.95, items: [
      { k: 'chip', text: 'Démo', size: 50, x: 540, y: 640, at: 0, shown: true },
      { k: 'text', text: 'Je tape', size: 130, x: 540, y: 820, at: 0, shown: true },
      { k: 'text', text: '2 km.', emph: '2 km.', emphAt: 0.5, size: 200, x: 540, y: 1010, at: 0, shown: true },
      { k: 'text', text: 'Regarde la plus petite', size: 86, x: 540, y: 1190, at: 0, shown: true },
      { k: 'text', text: 'boucle sortir.', emph: 'sortir.', emphAt: 1.2, size: 110, x: 540, y: 1310, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.0, to: 6.45, items: [
      { k: 'text', text: 'Regarde la boucle', size: 86, x: 540, y: 1180, at: 3.3 },
      { k: 'text', text: 'sortir.', emph: 'sortir.', emphAt: 4.2, size: 110, x: 540, y: 1300, at: 3.6 },
    ] },
    { type: 'board', from: 6.5, to: 10.0, items: [
      { k: 'text', text: 'Depuis ta porte,', size: 86, x: 540, y: 1180, at: 6.55 },
      { k: 'text', text: 'retour à ta porte.', emph: 'retour', emphAt: 7.6, size: 86, x: 540, y: 1295, at: 6.95 },
    ] },
    { type: 'board', from: 10.1, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 10.15 },
      { k: 'text', text: 'La plus', size: 120, x: 540, y: 850, at: 10.3 },
      { k: 'text', text: 'petite.', emph: 'petite.', emphAt: 10.9, size: 120, x: 540, y: 985, at: 10.55 },
      { k: 'check', s: 100, x: 540, y: 1130, at: 10.9 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 11.5, size: 96, x: 540, y: 1280, at: 11.3 },
      { k: 'chip', text: '2 km. Tapés.', size: 46, x: 540, y: 1405, at: 11.8 },
    ] },
  ],
  music: { bed: 'labo', offset: 20 },
  sfx: { swish: 0, accents: 0, extra: [[3.25, 'pop', -7], [5.6, 'thud', -7], [10.2, 'pop', -6], [11.3, 'thud', -5]] },
};

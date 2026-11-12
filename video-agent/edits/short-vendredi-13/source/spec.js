// Short muet (papier seul) pour Traceo, menu du 12/11/2026, script s01 « Vendredi 13 » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : le contre-pied (#22 Contrarian Flip).
// Beats : 0 accroche · 3 sauf ta boucle de 7 km · 7 rues jamais courues · 9 tracées en 10 s · 11 retour à ta porte + lien en bio.
// Identité propre : papier nuit prune #17141C, encre ivoire #EFE9DF, accent turquoise Traceo #3CC79A, Lora Bold, lit « nuit-blanche ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Vendredi 13, ça porte malheur. Sauf à ta boucle de 7 km.',
  silent: true, duration: 14,
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  scenes: [
    { type: 'board', from: 0, to: 2.9, items: [
      { k: 'text', text: 'VENDREDI 13', emph: 'VENDREDI 13', emphAt: 0, size: 60, x: 540, y: 680, at: 0, shown: true },
      { k: 'text', text: 'Vendredi 13,', emph: '13,', emphAt: 0.3, size: 150, x: 540, y: 880, at: 0, shown: true },
      { k: 'text', text: 'ça porte', size: 120, x: 540, y: 1050, at: 0, shown: true },
      { k: 'text', text: 'malheur.', size: 150, x: 540, y: 1210, at: 0.4 },
    ] },
    { type: 'board', from: 3.0, to: 6.9, items: [
      { k: 'text', text: 'Sauf à ta boucle', emph: 'Sauf', emphAt: 3.4, size: 104, x: 540, y: 700, at: 3.1 },
      { k: 'counter', value: 7, fromValue: 0, countFrom: 3.8, countTo: 4.9, unit: ' km', size: 260, x: 540, y: 950, at: 3.6 },
      { k: 'text', text: 'depuis chez toi.', emph: 'chez toi.', emphAt: 5.7, size: 92, x: 540, y: 1200, at: 5.3 },
    ] },
    { type: 'board', from: 7.0, to: 8.95, items: [
      { k: 'text', text: 'Des rues', size: 130, x: 540, y: 760, at: 7.05 },
      { k: 'text', text: 'que tu n\'as', size: 110, x: 540, y: 920, at: 7.3 },
      { k: 'text', text: 'jamais courues.', emph: 'jamais', emphAt: 8.0, size: 110, x: 540, y: 1070, at: 7.6 },
    ] },
    { type: 'board', from: 9.0, to: 10.9, items: [
      { k: 'text', text: 'Tracées en', size: 110, x: 540, y: 720, at: 9.05 },
      { k: 'counter', value: 10, fromValue: 0, countFrom: 9.3, countTo: 10.0, unit: ' s', size: 250, x: 540, y: 960, at: 9.15 },
      { k: 'text', text: 'environ.', size: 80, x: 540, y: 1180, at: 10.1 },
    ] },
    { type: 'board', from: 11.0, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 660, at: 11.05 },
      { k: 'text', text: 'Retour à ta porte.', emph: 'ta porte.', emphAt: 11.6, size: 100, x: 540, y: 880, at: 11.15 },
      { k: 'check', s: 100, x: 540, y: 1030, at: 11.7 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 12.4, size: 96, x: 540, y: 1180, at: 12.1 },
      { k: 'text', text: 'Vendredi 13 : conjuré.', size: 60, x: 540, y: 1330, at: 12.6 },
    ] },
  ],
  music: { bed: 'nuit-blanche', offset: 4 },
  sfx: { swish: 0, accents: 0, strike: 0, extra: [[0.3, 'thud', -6], [0.4, 'pop', -8], [3.1, 'pop', -8], [4.9, 'thud', -5], [5.3, 'pop', -8], [7.05, 'pop', -7], [9.1, 'pop', -7], [10.0, 'thud', -6], [11.1, 'pop', -6], [12.1, 'thud', -5]] },
};

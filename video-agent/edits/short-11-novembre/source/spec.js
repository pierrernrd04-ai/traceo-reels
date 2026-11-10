// Short muet (papier seul) pour Traceo, menu du 10/11/2026, script s01 « Le 11 novembre » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : la date butoir (#19 The Deadline), rendez-vous du calendrier.
// Beats : 0 le 11 novembre, c'est férié · 2.7 pas de réveil, pas d'excuse · 5.2 tu règles 15 km · 7.8 ta boucle sort en 10 s, depuis chez toi · 10.9 retour au départ + lien en bio.
// Identité propre : papier taupe clair #ECE7E1, encre bleu nuit #1A1F2E, accent rouge calendrier #C2412D, TeX Gyre Pagella Bold, lit « neon ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Le 11 novembre, c\'est férié. Ta boucle de 15 km sort en 10 secondes.',
  silent: true, duration: 14,
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  scenes: [
    { type: 'board', from: 0, to: 2.6, items: [
      { k: 'chip', text: 'Mercredi', size: 50, x: 540, y: 640, at: 0, shown: true },
      { k: 'text', text: 'Le 11 novembre,', emph: '11', emphAt: 0.3, size: 132, x: 540, y: 880, at: 0, shown: true },
      { k: 'text', text: 'c\'est férié.', emph: 'férié.', emphAt: 1.0, size: 150, x: 540, y: 1060, at: 0, shown: true },
    ] },
    { type: 'board', from: 2.7, to: 5.1, items: [
      { k: 'text', text: 'Pas de réveil.', size: 120, x: 540, y: 860, at: 2.75 },
      { k: 'text', text: 'Pas d\'excuse.', emph: 'excuse.', emphAt: 4.0, size: 120, x: 540, y: 1020, at: 3.6 },
    ] },
    { type: 'board', from: 5.2, to: 7.7, items: [
      { k: 'text', text: 'Tu règles', size: 120, x: 540, y: 800, at: 5.25 },
      { k: 'counter', value: 15, fromValue: 0, countFrom: 5.6, countTo: 6.6, unit: ' km', size: 260, x: 540, y: 1060, at: 5.5 },
    ] },
    { type: 'board', from: 7.8, to: 10.8, items: [
      { k: 'text', text: 'Ta boucle sort en', size: 104, x: 540, y: 780, at: 7.85 },
      { k: 'text', text: '10 secondes,', emph: '10 secondes,', emphAt: 8.6, size: 134, x: 540, y: 930, at: 8.2 },
      { k: 'text', text: 'depuis chez toi.', size: 104, x: 540, y: 1090, at: 9.0 },
    ] },
    { type: 'board', from: 10.9, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 10.95 },
      { k: 'text', text: 'Retour au départ.', emph: 'départ.', emphAt: 11.5, size: 104, x: 540, y: 860, at: 11.05 },
      { k: 'check', s: 100, x: 540, y: 1010, at: 11.6 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 12.3, size: 96, x: 540, y: 1160, at: 12.0 },
      { k: 'chip', text: 'Sortie du 11 novembre', size: 46, x: 540, y: 1300, at: 12.5 },
    ] },
  ],
  music: { bed: 'neon', offset: 12 },
  sfx: { swish: 0, accents: 0, strike: 0, extra: [[0.3, 'thud', -6], [2.8, 'pop', -8], [3.65, 'pop', -8], [5.3, 'pop', -8], [6.6, 'thud', -5], [8.6, 'thud', -6], [11.0, 'pop', -6], [12.0, 'thud', -5]] },
};

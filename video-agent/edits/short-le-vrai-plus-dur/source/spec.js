// Short muet (papier seul) pour Traceo, menu du 28/10/2026, script s01 « Le vrai plus dur ». Temps en secondes.
// Beats : 0 accroche (le plus dur de tes 5 km ?) · 3.1 pas courir, choisir où · 7.1 Traceo trace ta boucle en 10 s
// · 11.1 tu n'as plus qu'à sortir + lien en bio, écho « le plus dur » pour la boucle de relecture.
// Identité propre : papier abricot pâle, encre aubergine, accent bleu, Lora Bold + Archivo, lit musical « thriller ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Le vrai plus dur',
  silent: true, duration: 14,
  media: {},
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [],
  scenes: [
    { type: 'board', from: 0, to: 3.0, items: [
      { k: 'chip', text: 'Personne ne te le dit', size: 50, x: 540, y: 700, at: 0, shown: true },
      { k: 'text', text: 'Le plus dur', emph: 'plus dur', emphAt: 0.6, size: 150, x: 540, y: 900, at: 0, shown: true },
      { k: 'text', text: 'de tes', size: 120, x: 540, y: 1060, at: 0, shown: true },
      { k: 'text', text: '5 km ?', size: 190, x: 540, y: 1240, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.1, to: 7.0, items: [
      { k: 'text', text: 'Ce n\'est pas', size: 110, x: 540, y: 760, at: 3.15 },
      { k: 'text', text: 'courir.', size: 150, x: 540, y: 910, at: 3.45, strikeAt: 4.4 },
      { k: 'text', text: 'C\'est', size: 110, x: 540, y: 1080, at: 4.7 },
      { k: 'text', text: 'choisir où.', emph: 'choisir où.', emphAt: 5.5, size: 150, x: 540, y: 1230, at: 5.0 },
    ] },
    { type: 'board', from: 7.1, to: 11.0, items: [
      { k: 'logo', logo: TRACEO, s: 170, x: 540, y: 660, at: 7.15 },
      { k: 'text', text: 'Traceo trace', size: 110, x: 540, y: 860, at: 7.4 },
      { k: 'text', text: 'ta boucle en', size: 110, x: 540, y: 985, at: 7.7 },
      { k: 'counter', value: 10, fromValue: 0, clock: true, size: 170, x: 540, y: 1180, at: 8.1 },
      { k: 'chip', text: 'Depuis ta porte', size: 48, x: 540, y: 1360, at: 9.3 },
    ] },
    { type: 'board', from: 11.1, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 11.15 },
      { k: 'text', text: 'Toi, tu n\'as plus', size: 100, x: 540, y: 860, at: 11.3 },
      { k: 'text', text: 'qu\'à sortir.', emph: 'sortir.', emphAt: 12.0, size: 120, x: 540, y: 985, at: 11.6 },
      { k: 'check', s: 100, x: 540, y: 1130, at: 12.0 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 12.6, size: 96, x: 540, y: 1280, at: 12.4 },
      { k: 'chip', text: 'Le plus dur ? Réglé.', size: 46, x: 540, y: 1400, at: 12.9 },
    ] },
  ],
  music: { bed: 'thriller', offset: 24 },
  sfx: { swish: 0, accents: 0, extra: [[4.4, 'thud', -7], [8.1, 'tap', -8], [12.0, 'pop', -6], [12.4, 'thud', -5]] },
};

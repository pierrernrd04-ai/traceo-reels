// Short muet (papier seul) pour Traceo, menu du 01/11/2026, script s01 « 5 km ou 30 minutes » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : le face-à-face (#17 Head To Head), deux cartes côte à côte depuis la même porte.
// Beats : 0 accroche (tu cours 5 km ou 30 minutes ? regarde les 2 boucles) · 3.0 gauche : je règle 5 km · 6.0 droite : je règle 30 minutes
// · 8.6 deux boucles, depuis la même porte · 11.0 distance ou durée ? dis-le en commentaire.
// Identité propre : papier bleu glacier #E4ECEF, encre #14232B, accent terracotta #B5502A, TeX Gyre Schola, lit « enquete ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Tu cours 5 km ou 30 minutes ? Regarde les 2 boucles sortir.',
  silent: true, duration: 14,
  media: { carte: { src: 'assets/carte-duo.mp4', width: 900 } },
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [
    { id: 'carte', media: 'carte', offset: 0, from: 3.0, to: 10.9, pre: 0, ar: 1, keys: [[3.0, [100, 300, 740]]] },
  ],
  scenes: [
    { type: 'board', from: 0, to: 2.95, items: [
      { k: 'text', text: 'Tu cours', size: 104, x: 470, y: 660, at: 0, shown: true },
      { k: 'text', text: '5 km', emph: '5 km', emphAt: 0.4, size: 190, x: 470, y: 840, at: 0, shown: true },
      { k: 'text', text: 'ou 30 minutes ?', emph: '30 minutes ?', emphAt: 0.9, size: 96, x: 470, y: 1010, at: 0, shown: true },
      { k: 'text', text: 'Regarde les 2 boucles', size: 68, x: 470, y: 1180, at: 0, shown: true },
      { k: 'text', text: 'sortir.', emph: 'sortir.', emphAt: 1.4, size: 104, x: 470, y: 1295, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.0, to: 5.95, items: [
      { k: 'text', text: 'Gauche :', size: 84, x: 470, y: 1180, at: 3.2 },
      { k: 'text', text: 'je règle 5 km.', emph: '5 km.', emphAt: 4.0, size: 108, x: 470, y: 1300, at: 3.5 },
    ] },
    { type: 'board', from: 6.0, to: 8.55, items: [
      { k: 'text', text: 'Droite :', size: 84, x: 470, y: 1180, at: 6.1 },
      { k: 'text', text: 'je règle 30 minutes.', emph: '30 minutes.', emphAt: 6.9, size: 76, x: 470, y: 1300, at: 6.4 },
    ] },
    { type: 'board', from: 8.6, to: 10.9, items: [
      { k: 'text', text: 'Deux boucles,', size: 96, x: 470, y: 1180, at: 8.65 },
      { k: 'text', text: 'depuis la même porte.', emph: 'même porte.', emphAt: 9.4, size: 70, x: 470, y: 1300, at: 8.95 },
    ] },
    { type: 'board', from: 11.0, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 470, y: 650, at: 11.05 },
      { k: 'text', text: 'Distance', size: 120, x: 470, y: 850, at: 11.2 },
      { k: 'text', text: 'ou durée ?', emph: 'durée ?', emphAt: 11.8, size: 120, x: 470, y: 985, at: 11.45 },
      { k: 'text', text: 'Dis-le en commentaire.', emph: 'commentaire.', emphAt: 12.5, size: 74, x: 470, y: 1150, at: 12.0 },
      { k: 'chip', text: '2 à 42 km · 10 min à 4 h', size: 44, x: 470, y: 1290, at: 12.5 },
    ] },
  ],
  music: { bed: 'enquete', offset: 12 },
  sfx: { swish: 0, accents: 0, extra: [[3.3, 'pop', -7], [6.3, 'pop', -7], [8.8, 'thud', -7], [11.1, 'pop', -6], [12.0, 'thud', -5]] },
};

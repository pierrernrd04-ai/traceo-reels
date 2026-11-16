// Short muet (papier seul) pour Traceo, menu du 16/11/2026, script s01 « Lundi, 18 h 30 » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : la démo à froid (#18 Cold Open Demo).
// Beats : 0 accroche (lundi 18 h 30, je règle 30 min) · 3 carte : la boucle sort · 7 depuis ma porte, rues jamais courues · 10 retour au départ + lien en bio.
// Identité propre : papier bleu crépuscule #1E2A44, encre crème #F4EFE6, accent orange #F08A4B, Carlito Bold, lit « dub ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Lundi, 18 h 30. Je règle 30 minutes. Regarde ma boucle sortir.',
  silent: true, duration: 13,
  media: { carte: { src: 'assets/carte-1830.mp4', width: 900 } },
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [
    { id: 'carte', media: 'carte', offset: 0, from: 3.0, to: 9.95, pre: 0, ar: 1, keys: [[3.0, [90, 300, 760]]] },
  ],
  scenes: [
    { type: 'board', from: 0, to: 2.95, items: [
      { k: 'text', text: 'LUNDI SOIR', emph: 'LUNDI SOIR', emphAt: 0, size: 56, x: 540, y: 660, at: 0, shown: true },
      { k: 'text', text: 'Lundi,', size: 150, x: 540, y: 820, at: 0, shown: true },
      { k: 'text', text: '18 h 30.', emph: '18 h 30.', emphAt: 0.2, size: 190, x: 540, y: 1000, at: 0, shown: true },
      { k: 'text', text: 'Je règle', size: 100, x: 540, y: 1180, at: 0.9 },
      { k: 'counter', value: 30, fromValue: 0, countFrom: 1.2, countTo: 2.0, unit: ' min', size: 150, x: 540, y: 1320, at: 1.0 },
    ] },
    { type: 'board', from: 3.0, to: 6.95, items: [
      { k: 'text', text: 'Regarde ma boucle', size: 96, x: 540, y: 1180, at: 3.15 },
      { k: 'text', text: 'sortir.', emph: 'sortir.', emphAt: 4.0, size: 120, x: 540, y: 1310, at: 3.6 },
    ] },
    { type: 'board', from: 7.0, to: 9.95, items: [
      { k: 'text', text: 'Depuis ma porte,', emph: 'ma porte,', emphAt: 7.4, size: 88, x: 540, y: 1170, at: 7.05 },
      { k: 'text', text: 'par des rues que je', size: 70, x: 540, y: 1275, at: 7.6 },
      { k: 'text', text: 'n\'ai jamais courues.', emph: 'jamais', emphAt: 8.4, size: 80, x: 540, y: 1365, at: 7.9 },
    ] },
    { type: 'board', from: 10.0, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 660, at: 10.05 },
      { k: 'text', text: 'Retour au départ.', emph: 'départ.', emphAt: 10.6, size: 104, x: 540, y: 880, at: 10.15 },
      { k: 'check', s: 100, x: 540, y: 1030, at: 10.7 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 11.4, size: 96, x: 540, y: 1180, at: 11.1 },
      { k: 'text', text: 'Lundi, 18 h 30 : réglé.', size: 60, x: 540, y: 1330, at: 11.6 },
    ] },
  ],
  music: { bed: 'dub', offset: 2 },
  sfx: { swish: 0, accents: 0, strike: 0, extra: [[0.2, 'thud', -6], [0.9, 'pop', -8], [2.0, 'thud', -6], [3.15, 'pop', -8], [6.0, 'thud', -6], [7.05, 'pop', -7], [8.95, 'pop', -7], [10.1, 'pop', -6], [11.1, 'thud', -5]] },
};

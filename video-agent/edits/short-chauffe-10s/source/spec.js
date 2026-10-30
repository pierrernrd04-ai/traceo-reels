// Short muet (papier seul) pour Traceo, menu du 30/10/2026, script s01 « 3 minutes de chauffe, 10 secondes de tracé » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : le temps qui s'effondre (#5 Time Collapse).
// Beats : 0 ta chauffe 03:00 · 3.1 ta boucle de 5 km 00:10 · 7.1 depuis ta porte, par des rues nouvelles · 10.1 lacets faits ? lien en bio.
// Identité propre : papier gris perle #E9EDF2, encre marine #10233A, accent bleu Traceo #2F86C2, Bricolage Grotesque 800, lit « compte-a-rebours ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: '3 minutes de chauffe, 10 secondes de tracé',
  silent: true, duration: 13,
  media: {},
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [],
  scenes: [
    { type: 'board', from: 0, to: 3.0, items: [
      { k: 'chip', text: 'Avant ton footing', size: 50, x: 540, y: 680, at: 0, shown: true },
      { k: 'text', text: 'Ta chauffe :', size: 130, x: 540, y: 880, at: 0, shown: true },
      { k: 'counter', value: 180, fromValue: 180, clock: true, hold: true, size: 230, x: 540, y: 1110, at: 0, shown: true },
      { k: 'text', text: '3 minutes.', emph: '3 minutes.', emphAt: 0.6, size: 110, x: 540, y: 1320, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.1, to: 7.0, items: [
      { k: 'text', text: 'Ta boucle', size: 130, x: 540, y: 760, at: 3.15 },
      { k: 'text', text: 'de 5 km :', size: 130, x: 540, y: 900, at: 3.45 },
      { k: 'counter', value: 10, fromValue: 0, clock: true, size: 230, x: 540, y: 1120, at: 3.9 },
      { k: 'text', text: '10 secondes.', emph: '10 secondes.', emphAt: 5.4, size: 110, x: 540, y: 1330, at: 5.0 },
    ] },
    { type: 'board', from: 7.1, to: 10.0, items: [
      { k: 'text', text: 'Depuis', size: 120, x: 540, y: 820, at: 7.15 },
      { k: 'text', text: 'ta porte,', emph: 'porte,', emphAt: 7.8, size: 120, x: 540, y: 955, at: 7.4 },
      { k: 'text', text: 'par des rues', size: 110, x: 540, y: 1110, at: 8.0 },
      { k: 'text', text: 'nouvelles.', emph: 'nouvelles.', emphAt: 8.8, size: 130, x: 540, y: 1245, at: 8.3 },
    ] },
    { type: 'board', from: 10.1, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 10.15 },
      { k: 'text', text: 'Lacets faits ?', size: 110, x: 540, y: 870, at: 10.3 },
      { k: 'check', s: 100, x: 540, y: 1020, at: 10.9 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 11.5, size: 100, x: 540, y: 1170, at: 11.2 },
      { k: 'chip', text: '3 min de chauffe. 10 s de tracé.', size: 44, x: 540, y: 1300, at: 11.8 },
    ] },
  ],
  music: { bed: 'compte-a-rebours', offset: 20 },
  sfx: { swish: 0, accents: 0, extra: [[3.9, 'tap', -8], [5.0, 'thud', -7], [10.9, 'pop', -6], [11.2, 'thud', -5]] },
};

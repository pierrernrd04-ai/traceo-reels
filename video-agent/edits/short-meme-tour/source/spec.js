// Short muet (papier seul) pour Traceo : « Tu cours encore le même tour ? ». Temps en secondes.
// Beats : 0 accroche déjà à l'écran · 3.7 le chiffre 156, barré · 7.5 la solution · 11.3 la preuve 10 s + appel à l'action.
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Tu cours encore le même tour ?',
  silent: true, duration: 15,
  media: {},
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [],
  scenes: [
    { type: 'board', from: 0, to: 3.6, items: [
      { k: 'chip', text: 'Coureurs', size: 49, x: 540, y: 720, at: 0, shown: true },
      { k: 'text', text: 'Tu cours encore', size: 116, x: 540, y: 940, at: 0, shown: true },
      { k: 'text', text: 'le même tour ?', emph: 'même tour ?', emphAt: 0.8, size: 132, x: 540, y: 1090, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.7, to: 7.4, items: [
      { k: 'counter', value: 156, suffix: ' fois', size: 257, x: 540, y: 890, at: 3.75, countFrom: 3.9, countTo: 5.0, strikeAt: 6.4, strikeW: 700 },
      { k: 'text', text: 'le même parcours par an', size: 71, x: 540, y: 1110, at: 4.9 },
      { k: 'chip', text: '3 sorties par semaine', size: 47, x: 540, y: 1240, at: 5.4 },
    ] },
    { type: 'board', from: 7.5, to: 11.2, items: [
      { k: 'logo', logo: TRACEO, s: 210, x: 540, y: 690, at: 7.55 },
      { k: 'text', text: 'Une boucle neuve', size: 107, x: 540, y: 910, at: 7.8 },
      { k: 'text', text: 'par des rues que tu', size: 78, x: 540, y: 1050, at: 8.6 },
      { k: 'text', text: "n'as jamais courues.", emph: 'jamais', emphAt: 9.4, size: 78, x: 540, y: 1145, at: 9.0 },
      { k: 'check', s: 110, x: 540, y: 1310, at: 10.1 },
    ] },
    { type: 'board', from: 11.3, items: [
      { k: 'counter', value: 10, suffix: ' s', size: 224, x: 540, y: 810, at: 11.35, countFrom: 11.5, countTo: 12.3 },
      { k: 'text', text: 'pour tracer ta boucle', size: 73, x: 540, y: 1010, at: 12.0 },
      { k: 'chip', text: 'Gratuit · sans appli', size: 51, x: 540, y: 1150, at: 12.6 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 13.4, size: 94, x: 540, y: 1330, at: 13.2 },
    ] },
  ],
  music: { bed: 'arpege', offset: 0 },
  sfx: { swish: 0, accents: 0, extra: [[6.4, 'thud', -6], [10.1, 'pop', -6], [13.2, 'thud', -5]] },
};

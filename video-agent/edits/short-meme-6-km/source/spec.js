// Short muet (papier seul) pour Traceo, menu du 21/10/2026, script s01 « Même 6 km » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : le face-à-face (#17 Head To Head), écran partagé gauche / droite.
// Beats : 0 accroche déjà à l'écran · 3.1 à gauche, le tour connu par cœur · 7.1 à droite, rues jamais courues · 11.1 même distance, autre sortie + lien en bio.
// Identité propre : papier crème, encre bleu nuit, accent bleu Traceo, titres en Bowlby One SC, texte DM Sans, lit musical « neon ».
const TRACEO = 'assets/logos/traceo.png';
const REPEAT = 'assets/icons/repeat.png';
const MAP = 'assets/icons/world-map.png';
window.SPEC = {
  title: 'Même 6 km. Ton tour habituel ou 6 km de rues neuves ?',
  silent: true, duration: 14,
  media: {},
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [],
  scenes: [
    { type: 'board', from: 0, to: 3.0, items: [
      { k: 'text', text: 'Même 6 km.', emph: '6 km.', emphAt: 0.5, size: 150, x: 540, y: 720, at: 0, shown: true },
      { k: 'text', text: 'Ton tour habituel', size: 84, weight: 700, x: 540, y: 900, at: 0, shown: true },
      { k: 'text', text: 'ou 6 km de', size: 84, weight: 700, x: 540, y: 1010, at: 0, shown: true },
      { k: 'text', text: 'rues neuves ?', emph: 'neuves ?', emphAt: 0.9, size: 116, x: 540, y: 1140, at: 0, shown: true },
      { k: 'chip', text: 'Gauche', size: 52, x: 330, y: 1330, at: 0, shown: true },
      { k: 'chip', text: 'Droite', size: 52, x: 750, y: 1330, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.1, to: 7.0, items: [
      { k: 'chip', text: 'À gauche', size: 52, x: 540, y: 640, at: 3.15 },
      { k: 'img', img: REPEAT, s: 170, shadow: false, x: 540, y: 820, at: 3.3, pop: .6 },
      { k: 'text', text: 'Le tour que', size: 104, x: 540, y: 1010, at: 3.5 },
      { k: 'text', text: 'tes jambes', size: 104, x: 540, y: 1130, at: 3.8 },
      { k: 'text', text: 'connaissent', size: 104, x: 540, y: 1250, at: 4.1 },
      { k: 'text', text: 'déjà.', emph: 'déjà.', emphAt: 4.9, size: 104, x: 540, y: 1370, at: 4.4, strikeAt: 6.2 },
    ] },
    { type: 'board', from: 7.1, to: 11.0, items: [
      { k: 'chip', text: 'À droite', size: 52, x: 540, y: 640, at: 7.15 },
      { k: 'img', img: MAP, s: 170, shadow: false, x: 540, y: 820, at: 7.3, pop: .6 },
      { k: 'text', text: 'Une boucle par', size: 96, x: 540, y: 1010, at: 7.5 },
      { k: 'text', text: 'des rues que tu', size: 96, x: 540, y: 1125, at: 7.8 },
      { k: 'text', text: "n'as jamais", emph: 'jamais', emphAt: 8.8, size: 104, x: 540, y: 1245, at: 8.1 },
      { k: 'text', text: 'courues.', size: 104, x: 540, y: 1365, at: 8.4 },
      { k: 'check', s: 90, x: 540, y: 1500, at: 9.6 },
    ] },
    { type: 'board', from: 11.1, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 11.15 },
      { k: 'text', text: 'Même distance,', size: 108, x: 540, y: 860, at: 11.3 },
      { k: 'text', text: 'autre sortie.', emph: 'autre', emphAt: 12.0, size: 116, x: 540, y: 990, at: 11.6 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 12.6, size: 96, x: 540, y: 1160, at: 12.3 },
      { k: 'chip', text: 'Gauche ou droite ?', size: 48, x: 540, y: 1300, at: 12.8 },
    ] },
  ],
  music: { bed: 'neon', offset: 36.9 },
  sfx: { swish: 0, accents: 0, extra: [[3.3, 'pop', -6], [6.2, 'thud', -7], [9.6, 'pop', -6], [12.3, 'thud', -5]] },
};

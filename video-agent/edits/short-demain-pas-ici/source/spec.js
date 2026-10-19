// Short muet (papier seul) pour Traceo, menu du 19/10/2026, script s03 « Demain, pas ici ». Temps en secondes.
// Beats : 0 accroche déjà à l'écran · 3.1 la mémoire des rues (hier, avant-hier barrés) · 7.1 il cherche ailleurs (2 à 42 km)
// · 11.1 boucle neuve + lien en bio, écho « Demain » pour la boucle de relecture.
// Identité propre : papier bleu froid, encre marine, accent bleu Traceo, titres en Instrument Serif, lit musical « enquete ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Demain, tu ne courras pas ici.',
  silent: true, duration: 14,
  media: {},
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [],
  scenes: [
    { type: 'board', from: 0, to: 3.0, items: [
      { k: 'chip', text: 'Ta prochaine sortie', size: 48, x: 540, y: 700, at: 0, shown: true },
      { k: 'text', text: 'Demain,', size: 150, x: 540, y: 900, at: 0, shown: true },
      { k: 'text', text: 'tu ne courras', size: 132, x: 540, y: 1050, at: 0, shown: true },
      { k: 'text', text: 'pas ici.', emph: 'pas ici.', emphAt: 0.7, size: 150, x: 540, y: 1200, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.1, to: 7.0, items: [
      { k: 'logo', logo: TRACEO, s: 170, x: 540, y: 660, at: 3.15 },
      { k: 'text', text: 'Traceo se souvient', size: 104, x: 540, y: 850, at: 3.4 },
      { k: 'text', text: 'des rues qu\'il t\'a', size: 92, x: 540, y: 975, at: 3.8 },
      { k: 'text', text: 'déjà proposées.', emph: 'déjà', emphAt: 4.4, size: 92, x: 540, y: 1085, at: 4.1 },
      { k: 'chip', text: 'Boucle d\'hier', size: 50, x: 540, y: 1240, at: 5.0, strikeAt: 5.8 },
      { k: 'chip', text: 'Boucle d\'avant-hier', size: 50, x: 540, y: 1340, at: 5.3, strikeAt: 6.1 },
    ] },
    { type: 'board', from: 7.1, to: 11.0, items: [
      { k: 'text', text: 'Alors à chaque', size: 120, x: 540, y: 820, at: 7.15 },
      { k: 'text', text: 'sortie, il cherche', size: 110, x: 540, y: 960, at: 7.5 },
      { k: 'text', text: 'ailleurs.', emph: 'ailleurs.', emphAt: 8.4, size: 150, x: 540, y: 1110, at: 7.9 },
      { k: 'chip', text: 'De 2 à 42 km', size: 52, x: 540, y: 1270, at: 9.0 },
      { k: 'chip', text: 'Ou de 10 min à 4 h', size: 52, x: 540, y: 1370, at: 9.4 },
    ] },
    { type: 'board', from: 11.1, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 11.15 },
      { k: 'text', text: 'Une boucle neuve', size: 116, x: 540, y: 860, at: 11.3 },
      { k: 'text', text: 'à chaque sortie.', size: 104, x: 540, y: 985, at: 11.6 },
      { k: 'check', s: 100, x: 540, y: 1130, at: 12.0 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 12.6, size: 96, x: 540, y: 1290, at: 12.4 },
      { k: 'chip', text: 'Demain : ailleurs', size: 46, x: 540, y: 1410, at: 12.9 },
    ] },
  ],
  music: { bed: 'enquete', offset: 42.7 },
  sfx: { swish: 0, accents: 0, extra: [[5.8, 'thud', -7], [12.0, 'pop', -6], [12.4, 'thud', -5]] },
};

// Short muet (papier seul) pour Traceo, menu du 27/10/2026, script s01 « Demain, une autre rue ». Temps en secondes.
// Beats : 0 accroche (1 rue courue ce soir) · 3.1 demain, 1 autre · 7.1 il se souvient des rues déjà proposées
// · 11.1 prochaine boucle différente + lien en bio, écho « Demain » pour la boucle de relecture.
// Identité propre : papier sauge pâle, encre vert nuit, accent sarcelle, Poppins SemiBold, lit musical « filature ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Demain, une autre rue',
  silent: true, duration: 14,
  media: {},
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [],
  scenes: [
    { type: 'board', from: 0, to: 3.0, items: [
      { k: 'chip', text: 'Ce soir', size: 50, x: 540, y: 720, at: 0, shown: true },
      { k: 'text', text: '1 rue', emph: '1 rue', emphAt: 0.6, size: 190, x: 540, y: 930, at: 0, shown: true },
      { k: 'text', text: 'courue', size: 130, x: 540, y: 1100, at: 0, shown: true },
      { k: 'text', text: 'ce soir.', size: 130, x: 540, y: 1240, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.1, to: 7.0, items: [
      { k: 'text', text: 'Demain,', size: 150, x: 540, y: 780, at: 3.15 },
      { k: 'text', text: 'Traceo t\'en', size: 104, x: 540, y: 940, at: 3.5 },
      { k: 'text', text: 'propose', size: 104, x: 540, y: 1060, at: 3.8 },
      { k: 'text', text: '1 autre.', emph: '1 autre.', emphAt: 4.6, size: 150, x: 540, y: 1220, at: 4.1 },
      { k: 'chip', text: 'La rue de ce soir', size: 48, x: 540, y: 1380, at: 5.3, strikeAt: 6.0 },
    ] },
    { type: 'board', from: 7.1, to: 11.0, items: [
      { k: 'logo', logo: TRACEO, s: 170, x: 540, y: 660, at: 7.15 },
      { k: 'text', text: 'Il se souvient', size: 110, x: 540, y: 860, at: 7.4 },
      { k: 'text', text: 'des rues déjà', size: 100, x: 540, y: 985, at: 7.8 },
      { k: 'text', text: 'proposées.', emph: 'proposées.', emphAt: 8.7, size: 120, x: 540, y: 1110, at: 8.1 },
      { k: 'chip', text: 'Déjà proposée', size: 48, x: 540, y: 1260, at: 9.0, strikeAt: 9.6 },
      { k: 'chip', text: 'Déjà proposée', size: 48, x: 540, y: 1360, at: 9.3, strikeAt: 9.9 },
    ] },
    { type: 'board', from: 11.1, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 11.15 },
      { k: 'text', text: 'Ta prochaine boucle', size: 96, x: 540, y: 860, at: 11.3 },
      { k: 'text', text: 'sera différente.', emph: 'différente.', emphAt: 12.0, size: 104, x: 540, y: 980, at: 11.6 },
      { k: 'check', s: 100, x: 540, y: 1125, at: 12.0 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 12.6, size: 96, x: 540, y: 1280, at: 12.4 },
      { k: 'chip', text: 'Demain : une autre rue', size: 46, x: 540, y: 1400, at: 12.9 },
    ] },
  ],
  music: { bed: 'filature', offset: 30 },
  sfx: { swish: 0, accents: 0, extra: [[6.0, 'thud', -7], [9.6, 'tap', -8], [12.0, 'pop', -6], [12.4, 'thud', -5]] },
};

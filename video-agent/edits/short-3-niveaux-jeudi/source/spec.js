// Short muet (papier seul) pour Traceo, menu du 11/11/2026, script s01 « Les 3 niveaux du jeudi » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : liste numérotée avec un favori (#11 Numbered With A Favourite).
// Beats : 0 accroche · 3 niveau 1 et 2 · 7 niveau 3 (6 km, 10 s) · 11 depuis chez toi + lien en bio.
// Identité propre : papier vert d'eau #E3EEEA, encre vert nuit #102A2A, accent orange #D9772B, TeX Gyre Bonum Bold, lit « filature ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: '3 niveaux de footing le jeudi soir. Tu es à lequel ?',
  silent: true, duration: 14,
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  scenes: [
    { type: 'board', from: 0, to: 2.9, items: [
      { k: 'chip', text: 'Jeudi soir', size: 50, x: 540, y: 660, at: 0, shown: true },
      { k: 'text', text: '3 niveaux', emph: '3', emphAt: 0.3, size: 160, x: 540, y: 880, at: 0, shown: true },
      { k: 'text', text: 'de footing.', size: 128, x: 540, y: 1050, at: 0, shown: true },
      { k: 'text', text: 'Tu es à lequel ?', emph: 'lequel ?', emphAt: 1.6, size: 96, x: 540, y: 1220, at: 1.2 },
    ] },
    { type: 'board', from: 3.0, to: 6.9, items: [
      { k: 'chip', text: 'Niveau 1', size: 50, x: 540, y: 680, at: 3.05 },
      { k: 'text', text: 'Le même parc.', size: 110, x: 540, y: 830, at: 3.2 },
      { k: 'chip', text: 'Niveau 2', size: 50, x: 540, y: 1030, at: 4.8 },
      { k: 'text', text: 'Le même parc,', size: 100, x: 540, y: 1170, at: 4.95 },
      { k: 'text', text: 'dans l\'autre sens.', emph: 'l\'autre sens.', emphAt: 5.8, size: 100, x: 540, y: 1300, at: 5.3 },
    ] },
    { type: 'board', from: 7.0, to: 10.9, items: [
      { k: 'chip', text: 'Niveau 3', size: 54, x: 540, y: 660, at: 7.05 },
      { k: 'counter', value: 6, fromValue: 0, countFrom: 7.4, countTo: 8.3, unit: ' km', size: 240, x: 540, y: 880, at: 7.2 },
      { k: 'text', text: 'par des rues neuves,', emph: 'neuves,', emphAt: 8.9, size: 90, x: 540, y: 1080, at: 8.4 },
      { k: 'text', text: 'tracés en 10 secondes.', emph: '10 secondes.', emphAt: 9.8, size: 82, x: 540, y: 1220, at: 9.2 },
    ] },
    { type: 'board', from: 11.0, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 660, at: 11.05 },
      { k: 'text', text: 'Depuis chez toi.', emph: 'chez toi.', emphAt: 11.6, size: 108, x: 540, y: 880, at: 11.15 },
      { k: 'check', s: 100, x: 540, y: 1030, at: 11.7 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 12.4, size: 96, x: 540, y: 1180, at: 12.1 },
      { k: 'chip', text: 'Niveau 3 débloqué', size: 46, x: 540, y: 1320, at: 12.6 },
    ] },
  ],
  music: { bed: 'filature', offset: 8 },
  sfx: { swish: 0, accents: 0, strike: 0, extra: [[0.3, 'thud', -6], [1.2, 'pop', -8], [3.1, 'pop', -8], [4.85, 'pop', -8], [7.1, 'thud', -5], [8.3, 'pop', -7], [9.8, 'thud', -6], [11.1, 'pop', -6], [12.1, 'thud', -5]] },
};

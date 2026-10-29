// Short muet (papier seul) pour Traceo, menu du 29/10/2026, script s01 « 40 minutes réglées » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : la démo à froid (#18 Cold Open Demo).
// Beats : 0 accroche (je règle 40 minutes, regarde la boucle) · 3.0 carte : durée 40 min, plusieurs itinéraires comparés
// · 7.0 celui qui a le plus de rues nouvelles est gardé, le coureur le suit · 11.1 retour à ta porte + lien en bio, écho « 40 minutes » (boucle).
// Identité propre : papier pierre #EEEFEA, encre #17202B, accent vert Traceo foncé, TeX Gyre Adventor, lit « arpege ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Je règle 40 minutes. Regarde la boucle qui sort.',
  silent: true, duration: 14,
  media: { carte: { src: 'assets/carte-40.mp4', width: 900 } },
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [
    { id: 'carte', media: 'carte', offset: 0, from: 3.0, to: 11.0, pre: 0, ar: 1, keys: [[3.0, [160, 340, 760]]] },
  ],
  scenes: [
    { type: 'board', from: 0, to: 2.95, items: [
      { k: 'chip', text: 'Démo', size: 50, x: 540, y: 640, at: 0, shown: true },
      { k: 'text', text: 'Je règle', size: 120, x: 540, y: 820, at: 0, shown: true },
      { k: 'text', text: '40 minutes.', emph: '40 minutes.', emphAt: 0.5, size: 160, x: 540, y: 990, at: 0, shown: true },
      { k: 'text', text: 'Regarde la boucle', size: 86, x: 540, y: 1170, at: 0, shown: true },
      { k: 'text', text: 'qui sort.', emph: 'sort.', emphAt: 1.2, size: 110, x: 540, y: 1300, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.0, to: 6.95, items: [
      { k: 'text', text: 'Traceo compare', size: 84, x: 540, y: 1220, at: 3.3 },
      { k: 'text', text: 'plusieurs', size: 84, x: 540, y: 1325, at: 3.6 },
      { k: 'text', text: 'itinéraires…', emph: 'itinéraires…', emphAt: 4.4, size: 84, x: 540, y: 1430, at: 3.9 },
    ] },
    { type: 'board', from: 7.0, to: 11.0, items: [
      { k: 'text', text: '…et garde celui qui a', size: 76, x: 540, y: 1220, at: 7.05 },
      { k: 'text', text: 'le plus de', size: 76, x: 540, y: 1320, at: 7.35 },
      { k: 'text', text: 'rues nouvelles.', emph: 'rues nouvelles.', emphAt: 8.2, size: 84, x: 540, y: 1425, at: 7.65 },
    ] },
    { type: 'board', from: 11.1, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 11.15 },
      { k: 'text', text: 'Retour', size: 110, x: 540, y: 850, at: 11.3 },
      { k: 'text', text: 'à ta porte.', emph: 'porte.', emphAt: 12.0, size: 110, x: 540, y: 975, at: 11.6 },
      { k: 'check', s: 100, x: 540, y: 1120, at: 12.0 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 12.6, size: 96, x: 540, y: 1270, at: 12.4 },
      { k: 'chip', text: '40 minutes. Réglées.', size: 46, x: 540, y: 1395, at: 12.9 },
    ] },
  ],
  music: { bed: 'arpege', offset: 30 },
  sfx: { swish: 0, accents: 0, extra: [[3.25, 'pop', -7], [6.0, 'thud', -7], [11.2, 'pop', -6], [12.4, 'thud', -5]] },
};

// Short muet (papier seul) pour Traceo, menu du 24/10/2026, script s01 « Mode nuit, 21 h » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : la démo à froid (#18 Cold Open Demo).
// Beats : 0 accroche déjà à l'écran · 3.0 carte : mode nuit activé, la boucle sort (carte contrastée) · 7.0 le coureur suit la boucle, guidage vocal (rues jamais courues) · 11.1 guidage vocal jusqu'au retour, lien en bio (boucle répétée = loop).
// Identité propre : papier nuit #0E151F, encre #E8EEF3, accent turquoise Traceo, Inter 800 + JetBrains Mono, lit « code-noir ».
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: '21 h, mode nuit activé. Regarde la boucle qui sort.',
  silent: true, duration: 14,
  media: { carte: { src: 'assets/carte-nuit.mp4', width: 900 } },
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [
    { id: 'carte', media: 'carte', offset: 0, from: 3.0, to: 11.0, pre: 0, ar: 1, keys: [[3.0, [160, 340, 760]]] },
  ],
  scenes: [
    { type: 'board', from: 0, to: 2.95, items: [
      { k: 'text', text: '21 h.', size: 230, x: 540, y: 640, at: 0, shown: true },
      { k: 'text', text: 'Mode nuit activé.', size: 92, x: 540, y: 860, at: 0, shown: true },
      { k: 'text', text: 'Regarde la boucle', size: 92, x: 540, y: 990, at: 0, shown: true },
      { k: 'text', text: 'qui sort.', emph: 'sort.', emphAt: 1.0, size: 120, x: 540, y: 1130, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.0, to: 6.95, items: [
      { k: 'text', text: 'Carte contrastée,', size: 80, x: 540, y: 1210, at: 3.4 },
      { k: 'text', text: 'lisible même', size: 80, x: 540, y: 1310, at: 3.7 },
      { k: 'text', text: 'dans le noir.', emph: 'noir.', emphAt: 4.6, size: 80, x: 540, y: 1410, at: 4.0 },
    ] },
    { type: 'board', from: 7.0, to: 11.0, items: [
      { k: 'text', text: 'Depuis chez toi,', size: 80, x: 540, y: 1210, at: 7.1 },
      { k: 'text', text: 'par des rues', size: 80, x: 540, y: 1310, at: 7.4 },
      { k: 'text', text: 'jamais courues.', emph: 'jamais', emphAt: 8.4, size: 80, x: 540, y: 1410, at: 7.7 },
    ] },
    { type: 'board', from: 11.1, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 640, at: 11.15 },
      { k: 'text', text: 'Guidage vocal', size: 104, x: 540, y: 850, at: 11.3 },
      { k: 'text', text: "jusqu'au retour.", emph: 'retour.', emphAt: 12.0, size: 104, x: 540, y: 975, at: 11.6 },
      { k: 'text', text: 'Ta boucle du soir :', size: 76, x: 540, y: 1150, at: 12.2 },
      { k: 'text', text: 'lien en bio.', emph: 'lien', emphAt: 12.9, size: 104, x: 540, y: 1280, at: 12.6 },
    ] },
  ],
  music: { bed: 'code-noir', offset: 87 },
  sfx: { swish: 0, accents: 0, extra: [[3.25, 'pop', -7], [6.4, 'thud', -7], [11.2, 'pop', -6], [12.6, 'thud', -5]] },
};

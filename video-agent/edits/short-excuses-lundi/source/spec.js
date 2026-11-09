// Short muet (papier seul) pour Traceo, menu du 09/11/2026, script s01 « Les excuses du lundi » (rang 1, sans choix de Pierre). Temps en secondes.
// Mécanique : liste avec favori (#11 Numbered With A Favourite), classement façon tier list.
// Beats : 0 accroche · 2.5 n°4 · 4.0 n°3 · 5.5 n°2 · 7.0 n°1 (la favorite) · 8.9 barrée · 9.6 la n°1 se règle en 10 s · 12.3 boucle neuve depuis chez toi + lien en bio.
// Identité propre : papier paille #F3ECCB, encre vert-noir #1D241F, accent vert #178A68, Caladea Bold, lit « compte-a-rebours » (payoff 9.6 s).
const TRACEO = 'assets/logos/traceo.png';
window.SPEC = {
  title: 'Tes 4 excuses du lundi soir, classées. La n°1 se règle en 10 secondes.',
  silent: true, duration: 15,
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  scenes: [
    { type: 'board', from: 0, to: 2.45, items: [
      { k: 'chip', text: 'Lundi, 19 h', size: 50, x: 540, y: 660, at: 0, shown: true },
      { k: 'text', text: 'Tes 4 excuses', emph: '4', emphAt: 0.3, size: 140, x: 540, y: 860, at: 0, shown: true },
      { k: 'text', text: 'du lundi soir,', size: 110, x: 540, y: 1010, at: 0, shown: true },
      { k: 'text', text: 'classées.', emph: 'classées.', emphAt: 1.0, size: 130, x: 540, y: 1160, at: 0, shown: true },
    ] },
    { type: 'board', from: 2.5, to: 9.45, items: [
      { k: 'text', text: '4. Il pleut.', size: 92, x: 540, y: 760, at: 2.55 },
      { k: 'text', text: '3. Il fait déjà nuit.', size: 92, x: 540, y: 900, at: 4.0 },
      { k: 'text', text: '2. J\'ai la flemme.', size: 92, x: 540, y: 1040, at: 5.5 },
      { k: 'text', text: '1. Je connais déjà', emph: '1.', emphAt: 7.1, size: 104, x: 540, y: 1215, at: 7.0, pop: .6 },
      { k: 'text', text: 'le parcours.', emph: 'le parcours.', emphAt: 7.6, size: 104, x: 540, y: 1345, at: 7.2, strikeAt: 8.9, strikeColor: 'ink' },
    ] },
    { type: 'board', from: 9.5, to: 12.25, items: [
      { k: 'text', text: 'La n°1', size: 130, x: 540, y: 820, at: 9.55 },
      { k: 'text', text: 'se règle en', size: 100, x: 540, y: 980, at: 9.75 },
      { k: 'text', text: '10 secondes.', emph: '10 secondes.', emphAt: 10.4, size: 130, x: 540, y: 1140, at: 10.0 },
    ] },
    { type: 'board', from: 12.3, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 12.35 },
      { k: 'text', text: 'Une boucle neuve,', emph: 'neuve,', emphAt: 12.9, size: 100, x: 540, y: 850, at: 12.45 },
      { k: 'text', text: 'depuis chez toi.', size: 100, x: 540, y: 975, at: 12.65 },
      { k: 'check', s: 100, x: 540, y: 1120, at: 13.0 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 13.6, size: 96, x: 540, y: 1270, at: 13.3 },
    ] },
  ],
  music: { bed: 'compte-a-rebours', offset: 86.4 },
  sfx: { swish: 0, accents: 0, strike: 0, extra: [[0.3, 'thud', -6], [2.6, 'pop', -8], [4.05, 'pop', -8], [5.55, 'pop', -8], [7.05, 'thud', -6], [9.6, 'pop', -6], [10.4, 'thud', -5], [12.4, 'pop', -6], [13.3, 'thud', -5]] },
};

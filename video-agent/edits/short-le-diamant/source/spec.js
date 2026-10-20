// Short muet (papier seul) pour Traceo, menu du 20/10/2026, script s01 « Le diamant » (rang 1, sans choix de Pierre). Temps en secondes.
// Beats : 0 accroche déjà à l'écran · 3.1 la révélation (31 jours de Premium) · 7.1 toutes les 100 sorties, un de plus
// · 11.1 première sortie + lien en bio, écho « diamant » pour la boucle de relecture.
// Identité propre : papier lilas, encre aubergine, accent turquoise profond, titres en Archivo Black, lit musical « sonar ».
const TRACEO = 'assets/logos/traceo.png';
const GEM = 'assets/icons/gem-stone.png';
const RUN = 'assets/icons/person-running.png';
window.SPEC = {
  title: '100 sorties = 1 diamant Traceo.',
  silent: true, duration: 14,
  media: {},
  layout: { keys: [[0, 1920]] },
  zoom: { keys: [[0, 1]] },
  actors: [],
  scenes: [
    { type: 'board', from: 0, to: 3.0, items: [
      { k: 'text', text: '100 sorties', size: 150, x: 540, y: 780, at: 0, shown: true },
      { k: 'text', text: '= 1 diamant', emph: 'diamant', emphAt: 0.5, size: 130, x: 540, y: 960, at: 0, shown: true },
      { k: 'img', img: GEM, s: 190, shadow: false, x: 540, y: 1150, at: 0, shown: true },
      { k: 'text', text: 'Voici ce qu\'il te donne.', size: 72, weight: 700, x: 540, y: 1330, at: 0, shown: true },
    ] },
    { type: 'board', from: 3.1, to: 7.0, items: [
      { k: 'img', img: GEM, s: 170, shadow: false, x: 540, y: 680, at: 3.15, pop: .6 },
      { k: 'text', text: 'Un diamant,', size: 110, x: 540, y: 880, at: 3.4 },
      { k: 'text', text: 'c\'est 31 jours', size: 120, x: 540, y: 1020, at: 3.8 },
      { k: 'text', text: 'de Premium.', emph: 'Premium.', emphAt: 4.6, size: 120, x: 540, y: 1160, at: 4.2 },
      { k: 'chip', text: 'Boucles par les petites rues', size: 46, x: 540, y: 1330, at: 5.2 },
    ] },
    { type: 'board', from: 7.1, to: 11.0, items: [
      { k: 'img', img: RUN, s: 150, shadow: false, x: 540, y: 660, at: 7.15 },
      { k: 'text', text: 'Toutes les', size: 110, x: 540, y: 850, at: 7.3 },
      { k: 'text', text: '100 sorties,', size: 130, x: 540, y: 990, at: 7.6 },
      { k: 'text', text: 'un de plus.', emph: 'un de plus.', emphAt: 8.6, size: 130, x: 540, y: 1130, at: 8.0 },
      { k: 'chip', text: 'Sortie 100 : 1 diamant', size: 48, x: 540, y: 1290, at: 9.0 },
      { k: 'chip', text: 'Sortie 200 : 2 diamants', size: 48, x: 540, y: 1390, at: 9.5 },
    ] },
    { type: 'board', from: 11.1, items: [
      { k: 'logo', logo: TRACEO, s: 190, x: 540, y: 650, at: 11.15 },
      { k: 'text', text: 'Ta 1re sortie', size: 116, x: 540, y: 860, at: 11.3 },
      { k: 'text', text: 'commence ici.', size: 110, x: 540, y: 990, at: 11.6 },
      { k: 'text', text: 'Lien en bio', emph: 'Lien', emphAt: 12.4, size: 96, x: 540, y: 1150, at: 12.1 },
      { k: 'chip', text: 'Prochain arrêt : ton diamant', size: 46, x: 540, y: 1290, at: 12.7 },
    ] },
  ],
  music: { bed: 'sonar', offset: 0 },
  sfx: { swish: 0, accents: 0, extra: [[3.2, 'pop', -6], [9.0, 'thud', -7], [9.5, 'thud', -7], [12.1, 'pop', -5]] },
};

# Pilote automatique Traceo (Instagram + YouTube Shorts + Pinterest)

Ce fichier est le mode d'emploi de la tâche planifiée quotidienne. Il décrit la boucle
**mesurer → analyser → repérer → créer → publier → noter**, avec uniquement des outils gratuits
(Metricool, ce studio vidéo, ce dépôt GitHub). Tout ce qui suit s'applique à chaque exécution.

## 1. Repères

| Élément | Valeur |
|---|---|
| Fondateur | Pierre (tutoiement, réponses en français) |
| Produit | Traceo, https://traceorun.pages.dev (lien d'appli direct : https://traceorun.pages.dev/app?go=1) |
| Metricool | marque `blogId` / `brandId` = `7326703`, fuseau `Europe/Paris` |
| Instagram | `traceo.io` (Reels) |
| YouTube | chaîne `UCe7z8gaFyNoiSqqJxpBg6Nw` (Shorts) |
| Hébergement vidéo | ce dépôt, fichiers à la racine, URL `https://raw.githubusercontent.com/pierrernrd04-ai/traceo-reels/main/<fichier>.mp4` |
| Registre | `studio/registre.json` (toutes les vidéos, leurs dates de publication et leurs résultats) |
| Stratégie | doc https://claude.ai/code/artifact/6b7715cc-af36-4905-a993-21c4527f5756 |

## 2. Faits produit autorisés (n'en invente aucun autre)

- Trace une boucle de course à pied depuis chez toi, par des rues que tu n'as jamais courues, et te ramène au départ.
- Distance de 2 à 42 km, ou durée de 10 min à 4 h. Environ 10 secondes pour tracer.
- Compare plusieurs itinéraires et garde celui qui a le plus de rues nouvelles ; se souvient des rues déjà proposées.
- Guidage vocal ; carte contrastée et mode nuit ; image néon de la boucle à partager.
- Export Strava, Garmin et GPX.
- Partout en France, Corse et outre-mer compris. Dans le navigateur du téléphone, sans appli à télécharger, sans compte pour la première sortie.
- Premium : 4,99 € pour 31 jours, sans abonnement. Boucles par les petites rues (Premium). Bouton « Je pars courir » qui prévient les coureurs à moins de 5 km, positions arrondies, mode invisible, messages (Premium). Un diamant toutes les 100 sorties = 31 jours de Premium.

Interdits : chiffres d'utilisateurs, témoignages, avis ou statistiques inventés ; « garanti » ; cibler les
marcheurs ou randonneurs tant que Pierre n'a pas confirmé que Traceo les gère (les Reels v07 et v08 sont en
brouillon pour ça) ; toute promesse de récompense pour le défi #UneRueParSortie tant que Pierre ne l'a pas fixée.
Une illustration (carte, ville, boucle) reste une illustration : écris « (Illustration) » dans la légende si elle peut passer pour une vraie donnée.

## 3. Charte des vidéos

- 4K vertical 2160×3840, 30 i/s, 12 à 17 s. Accroche lisible dans la première seconde. Fin sur la carte de marque (`endcard`) avec le logo spirale et le mot-symbole « traceo » (o en turquoise).
- Professionnel, moderne, minimaliste. Jamais d'univers enfantin.
- **Chaque vidéo a sa propre police, sa propre palette et sa propre musique.** Les polices déjà utilisées sont dans `engine.F` : prends-en une autre (`fc-list : family`) ou change franchement de combinaison.
- Turquoise `#3CC79A` et bleu `#4AA6D8` restent les couleurs de marque (logo, boucle Traceo, appels à l'action).
- Zone sûre du texte : x 150 → 1700, y 520 → 2860 (rien sous l'interface Instagram). Texte principal ≥ 70 px.
- Son : musique synthétisée (`audio10.py`, `audio_w2.py` ou une nouvelle fonction dans un nouveau fichier `audio_wN.py`), signature sonore `sonic_logo` sur la carte de fin, effets avec `sfx.add_sfx`, mastering −14 LUFS (déjà fait par `finish`).

### Fabriquer une vague

1. Écris `studio/scenes_wN.py` sur le modèle de `scenes_w2.py` : une classe par vidéo avec `name`, `duration`, `end_t`, `song`, éventuellement `sfx` (liste `(t, "pop"|"send"|"type"|"coin"|"thud"|"tick"|"ding"|"swoosh"|"print")`), une méthode `frame(t)` qui renvoie une image `uint8 (3840, 2160, 3)`, et une liste `SCENES_WN`.
2. Copie `render_w2.py` en `render_wN.py` (imports `scenes_wN`, sortie `outN/`).
3. **Contrôle visuel obligatoire avant le rendu** : pour chaque vidéo, enregistre 5 à 6 images clés réduites
   (`PIL.Image.fromarray(sc.frame(t)).resize((540, 960)).save(...)` dans `studio/apercus/`) et regarde-les avec l'outil Read.
   Corrige tout texte qui se chevauche, sort de la zone sûre ou est coupé, puis recommence jusqu'à ce que ce soit propre.
4. Rendu : `python3 render_wN.py 0 1 2 3` (environ 1 à 2 min par vidéo). Vérifie avec `ffprobe` : 2160×3840, piste audio présente.
5. Copie les MP4 à la racine du dépôt sous le nom `traceo-wN-xx-sujet.mp4`.

## 4. La boucle quotidienne (chaque jour vers 17 h 10, publication vers 18 h)

Pierre a donné le 19/10/2026 son accord permanent pour que ce pilote crée et publie **chaque jour**, sans
validation préalable, des vidéos conformes à ce fichier, sur ses comptes Traceo. Tout doit rester gratuit.

### Quotas gratuits à respecter (vérifiés le 19/10/2026)

- **Metricool gratuit : 20 publications par mois au total** (tous réseaux confondus, comptées au mois de publication ;
  au-delà, elles ne partent pas). Les brouillons ne comptent pas. Octobre 2026 est déjà plein (20/20) : n'ajoute rien en octobre.
  Avant toute programmation Metricool, compte les publications non brouillon du mois concerné avec `getScheduledPosts`
  (plus celles déjà publiées ce mois-ci, visibles dans les statistiques) et ne dépasse jamais 20.
- **Metricool gratuit : 5 concurrents Instagram** fixés par Pierre dans l'interface (ta liste de veille, gratuite).
- **vidIQ gratuit : 150 crédits par mois** (recharge le 13 de chaque mois). Recherche d'outliers = 5 crédits ; publication
  d'un Reel Instagram = 0 crédit ; import d'une vidéo (`vidiq_video_upload`) = 0 crédit.

### Étapes de chaque jour

**A. Mesurer.** Avec Metricool `getAnalyticsDataByMetrics` (brandId 7326703), sur les 28 derniers jours :
Instagram Reels `IGRE02` (date), `IGRE03` (texte), `IGRE06` (url), `IGRE23` (vues), `IGRE11` (couverture),
`IGRE21` (partages), `IGRE12` (enregistrements), `IGRE07` (commentaires), `IGRE10` (j'aime), `IGRE24` (durée
moyenne de visionnage), `IGRE27` (rétention), `IGRE28` (taux de vue >3 s). Pour YouTube, appelle d'abord
`getAnalyticsAvailableMetrics` (network youtube) et prends les champs **non dépréciés**. Rattache chaque publication à
sa vidéo du registre (date + texte) et écris les chiffres dans `resultats` (une clé par date de relevé).

**B. Analyser.** Score = (partages + 0,8 × enregistrements + 0,5 × commentaires) pour 1 000 comptes atteints,
départagé par la rétention. Ignore les vidéos publiées depuis moins de 48 h. Tiens à jour le top 3 et le flop 3
dans `studio/registre.json` (clé `analyse`).

**C. Repérer ce qui marche ailleurs (gratuit).**
1. Liste de veille Metricool : `getAnalyticsDataByMetrics` avec `IGCR01` (compte), `IGCR03` (texte), `IGCR04` (url),
   `IGCR06` (date), `IGCR07` (j'aime), `IGCR08` (commentaires), `IGCR09` (interactions), `IGCR10` (engagement), sur 30 jours.
   Repère les 3 Reels qui dépassent le plus la moyenne de leur propre compte. Note dans `registre.json` (clé `veille`)
   leur accroche, leur format et pourquoi ils marchent. Si aucun concurrent n'est configuré, dis-le dans le rapport.
2. vidIQ : une fois par jour, si `vidiq_balance` ≥ 5, `vidiq_instagram_tiktok_outlier_search` avec
   `query` « running course à pied parcours », `audienceQuery` « Culture/Region: France/French; Global: false; Demographics: coureurs amateurs 20-45 ans; »,
   `descriptionLanguage` ["fr"], `resultsPerPlatform` 5. Garde les accroches et formats qui reviennent au moins deux fois.
3. Si un connecteur Kapturz ou Virlo est un jour disponible, utilise-le en plus.
Ne copie jamais une vidéo : reprends la mécanique (accroche, structure, format) et applique-la à Traceo avec ses vrais faits.

**D. Créer.** Garde en stock au moins 3 vidéos prêtes qui ne sont pas encore parues sur Instagram (hors v07/v08).
S'il en manque, fabrique-en 1 (2 au maximum) par jour, en t'inspirant d'abord de ton top 3 puis de la veille.
Une nouvelle vague = un nouveau fichier `scenes_wN.py` (tu peux y ajouter des vidéos au fil des jours).

**E. Publier.**
- **Instagram, 1 Reel par jour.** Si aucun Reel n'est programmé dans Metricool pour aujourd'hui (les brouillons ne comptent pas)
  et qu'aucun n'est déjà paru aujourd'hui : publie maintenant via vidIQ, gratuitement :
  1. `vidiq_instagram_connected_accounts` → prends le compte `traceo.io` avec `publishingAvailable: true`.
     S'il n'y en a pas, saute la publication et mets en tête du rapport : « Connecte traceo.io à vidIQ (app.vidiq.com) pour activer la publication quotidienne ».
  2. `vidiq_video_upload` avec l'URL raw GitHub de la vidéo → `videoUrl`.
  3. `vidiq_instagram_publish_reel` avec ce `videoUrl`, le `platformAccountId`, la légende (règles ci-dessous), sans `trialParams`
     et sans `isAiGenerated` ; continue avec `containerId` / `mcpJobId` jusqu'à `PUBLISHED`. Ne relance pas une publication en échec.
- **YouTube Shorts via Metricool**, dans la limite du quota mensuel : chaque nouvelle vidéo y va aussi, à 18:00, un jour sans Short programmé.
- **Pinterest via Metricool**, seulement si un compte Pinterest est connecté (`getBrandSettings`) et s'il reste du quota après YouTube.
- Programmation Metricool : `createScheduledPost`, `autoPublish: true`, `draft: false`, média = URL raw GitHub (après `git push`), date au moins 24 h dans le futur.
- Légende Instagram : 1re ligne = une seule action (envoie-le à…, enregistre-le…, commente…, ou « Trace ta boucle gratuite : lien en bio. »),
  puis 2 à 3 phrases avec les mots que les gens cherchent (parcours de course à pied, running, footing), puis 4 hashtags maximum.
- YouTube : `youtubeData {"title": "<accroche + mot-clé> #running", "type": "short", "privacy": "public", "madeForKids": false, "category": "SPORTS", "tags": [15 tags], "isAiGeneratedContent": false}`.
  Description = 1re phrase riche en mots-clés + texte de la vidéo + une question pour les commentaires, puis **ce bloc exact** :

```
———
TRACEO · Une boucle de course neuve à chaque sortie

Traceo trace un parcours de course à pied depuis chez toi, par des rues que tu n'as jamais courues, et te ramène à ton point de départ. Choisis une distance de 2 à 42 km ou une durée de 10 min à 4 h : en 10 secondes environ, Traceo compare plusieurs itinéraires et garde celui qui a le plus de rues nouvelles.

· Guidage vocal pendant ta sortie
· Mode nuit et carte contrastée
· Export Strava, Garmin et GPX
· Partout en France, Corse et outre-mer compris
· Dans le navigateur de ton téléphone, sans appli à télécharger

Gratuit pour commencer, sans compte pour ta première sortie. Premium : 4,99 € pour 31 jours, sans abonnement.

→ Trace ta boucle gratuite : https://traceorun.pages.dev
→ Instagram : https://www.instagram.com/traceo.io/
→ Abonne-toi pour une nouvelle idée de parcours à chaque Short.

#running #courseapied #footing #parcoursrunning #shorts
```

- Pinterest : `pinterestData {"boardId": "<nom exact du tableau>", "pinTitle": "<titre avec mots-clés>", "pinLink": "https://traceorun.pages.dev"}`.
  Tableaux : « Parcours de course à pied », « Motivation running », « Courir en ville », « Courir le soir et l'hiver », « Défi #UneRueParSortie ».
- Vérifie chaque programmation avec `getScheduledPosts`.

**F. Noter.** Mets à jour `studio/registre.json` (vidéos, dates par réseau, résultats, analyse, veille, compteur Metricool du mois),
commit et push. Auteur des commits : `Pierre Renard <pierre.rnrd04@gmail.com>`. Avant de pousser : `git pull --rebase`.

## 5. Ce que le pilote ne fait jamais

- Supprimer ou modifier une publication déjà en ligne, ou une publication programmée qu'il n'a pas créée lui-même.
- Dépasser 20 publications Metricool dans un mois, ou dépenser des crédits vidIQ au-delà d'une recherche par jour.
- Publier les brouillons v07 / v08, répondre à des commentaires, envoyer des messages, payer quoi que ce soit, prendre un essai payant.
- Contourner une erreur d'autorisation : il s'arrête sur ce point et le signale.

## 6. Rapport à Pierre (message final, court, lisible sur téléphone)

Du mardi au dimanche, 3 lignes :
```
✅ Publié aujourd'hui : <vidéo> sur <réseaux> (ou « rien, et pourquoi »)
📈 Hier : meilleure vidéo <titre> · <chiffre clé>
👉 Action pour toi : <une seule, ou « aucune »>
```
Le lundi, le bilan de la semaine :
```
📊 Semaine du JJ/MM : X vues IG · Y vues YT
🏆 Top : <vidéo> (<chiffre clé>) — pourquoi en une phrase
📉 Flop : <vidéo> — pourquoi en une phrase
🔭 Veille : <la mécanique qui marche chez les autres cette semaine>
🎬 Créées : N vidéos · 📅 Quota Metricool du mois : X/20
👉 Une seule action pour toi (s'il y en a une)
```

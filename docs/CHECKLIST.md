# Rubik — Travail à deux, full Python

Références : [contrat](CONVENTIONS.md), [sujet conservé](SUJET.md),
[points à vérifier conservés](POINTS_A_VERIFIER.md).

## 1. Modèle commun — ensemble

- [ ] Définir les six couleurs avec une Enum.
- [ ] Fixer les positions des 12 arêtes et 8 coins et l'ordre des stickers.
- [ ] Fournir un état résolu et le parser de mouvements.
- [ ] Implémenter les 18 mouvements sans dépendance graphique.
- [ ] Vérifier les mouvements avec des états attendus indépendants.
- [ ] Tester quatre quarts de tour, deux demi-tours et mouvement + inverse.
- [ ] Implémenter import/export JSON et validation des états impossibles.
- [ ] Fixer le repère des algorithmes CFOP par rapport aux couleurs.
- [ ] Vérifier que chaque propriétaire peut avancer avec les mêmes fixtures.

## 2. Solver — neon_05

- [ ] Initialiser l'état à partir du mélange.
- [ ] Cross : placer et orienter les quatre arêtes de croix.
- [ ] F2L : résoudre les quatre paires coin/arête.
- [ ] OLL : orienter la dernière couche.
- [ ] PLL : permuter la dernière couche et terminer l'alignement.
- [ ] Vérifier les postconditions sans casser les étapes précédentes.
- [ ] Adapter les algorithmes à U/R/F/D/L/B sans M/E/S/x/y/z.
- [ ] Documenter les cas et algorithmes dans data/cfop/.
- [ ] Simplifier les mouvements adjacents sans changer leur effet.
- [ ] Renvoyer une liste de mouvements puis une seule ligne sur stdout.
- [ ] Gérer cube résolu, erreurs et cas non encore couverts.
- [ ] Mesurer CFOP en Python : moyenne ≤ 50 HTM, temps total ≤ 3 s.
- [ ] Optimiser les choix F2L et enchaînements si les mesures dépassent la cible.

## 3. Renderer — nicolsan

- [ ] Choisir et documenter la bibliothèque graphique.
- [ ] Lire l'état initial et les mouvements fournis sur stdin.
- [ ] Proposer un mode logs pour tester avant la 3D.
- [ ] Dessiner les cubies, centres et stickers au bon endroit.
- [ ] Ajouter caméra orbitale, zoom et éclairage lisible.
- [ ] Animer chaque couche, puis figer précisément sa nouvelle position.
- [ ] Afficher le mouvement courant et la progression.
- [ ] Ajouter pause, reprise, pas suivant/précédent et retour au début.
- [ ] Respecter vitesse et délai configurables.
- [ ] Vérifier l'état final ; signaler une séquence valide qui ne résout pas.
- [ ] Refuser une entrée invalide sans animer une séquence partielle.
- [ ] Garder un état logique indépendant des flottants de l'animation.

## 4. Intégration — ensemble

- [ ] Même mélange → même état initial dans les deux parties.
- [ ] Solver → fichier de mouvements → renderer.
- [ ] Fixtures d'états intermédiaires et finaux pour détecter les désaccords.
- [ ] Vérifier une solution par simulation et par états de référence.
- [ ] Tester les erreurs, le superflip et des mélanges reproductibles variés.
- [ ] Bench chronométré dans un nouveau processus, démarrage Python compris.
- [ ] Le solver fonctionne sans bibliothèque graphique et sans fenêtre.
- [ ] Tests depuis un clone propre sur la machine de l'école.
- [ ] Mettre à jour les instructions au fur et à mesure des fonctions réalisées.
- [ ] Chacun sait expliquer le modèle, les rotations et CFOP.

Seule l’arborescence est préparée : tous les fichiers Python sont des TODO,
y compris les tests. Aucune fonctionnalité n’est encore implémentée. Les références SUJET.md et POINTS_A_VERIFIER.md
restent inchangées ; leurs anciennes mentions C++ se lisent avec cette checklist.

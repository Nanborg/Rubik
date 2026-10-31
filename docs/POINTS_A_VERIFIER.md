# Rubik — Points à vérifier

À relire avant la soutenance. Si un point **bloquant** échoue : on arrête tout.

## Avant de commencer (bloquant)

- [ ] Le dépôt Git existe et correspond au projet.
- [ ] Pas de triche : chacun sait **expliquer le code**.
- [ ] Fichier `author` présent.
- [ ] Chaque bibliothèque utilisée est justifiée (aucune : bibliothèque standard seulement).

## Partie obligatoire

| Test | À essayer | Bloquant |
|---|---|---|
| Gestion d'erreurs | sans argument, trop d'arguments, mouvement invalide, séquence invalide | non |
| Position simple | 4-5 mouvements : juste, en 2-3 s | **oui** |
| Position complexe | 5 à 20 mouvements : juste, en 2-3 s | **oui** |
| Position aléatoire | plus de 20 mouvements : juste, en 2-3 s | **oui** |
| Performance | plus de 30 mouvements : moyenne et temps | note sur 5 |
| Distance-20 | superflip (voir ci-dessous) | non |

**Performance :**
- Ces points demandent une moyenne < 150 mouvements.
- Le sujet demande une moyenne ≤ **50**. On vise 50 (idéal : < 30).
- Temps : < 2-3 s, **affichage compris**.

**Superflip :**
`U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2`

Autres cas : http://www.cube20.org/distance20s/

## Bonus (seulement si l'obligatoire est parfait)

Idées bien notées :
- Interface 3D avec la solution pas à pas.
- Moyenne < 30 mouvements en quelques secondes.
- Plusieurs algorithmes, ou choix du meilleur.
- Autres puzzles (2x2x2, 4x4x4, Megaminx…).
- Générateur de mélanges.
- Solution en étapes compréhensibles.

Option bonus = argument qui commence par `-`.

À la soutenance : on résout un vrai cube (moins de 30-40 s = très impressionnant).

## Avant la soutenance (à tester nous-mêmes)

- [ ] Tout cloner dans un dossier vide, puis `make`, `./rubik "F R U2 B' L' D'"`.
- [ ] Les erreurs : aucun crash, aucune trace Python.
- [ ] Mélanges de 1 à 40 mouvements, tous résolus.
- [ ] Superflip résolu en un temps normal.
- [ ] Pas de fuite mémoire (`valgrind` sur les tests C++).
- [ ] Pas de boucle infinie, pas de segfault.
- [ ] On sait expliquer l'algorithme avec des mots simples et des schémas.

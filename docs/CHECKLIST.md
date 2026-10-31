# Rubik (42) — Architecture et checklist du binôme

## 1. Objectif et contraintes

Créer un programme `rubik` qui reçoit en argument une séquence de mélange d'un Rubik's Cube 3×3×3 et affiche une séquence de résolution en notation officielle (`F R U B L D`, avec les suffixes `'` et `2`).

**Contraintes du sujet :**
- Ne pas simplement inverser le mélange.
- Viser une **moyenne de 50 mouvements** selon la métrique HTM (un quart de tour ou un demi-tour compte pour un mouvement).
- Répondre en **3 secondes maximum**.
- Gérer correctement les entrées invalides et les erreurs.
- Ne pas utiliser de bibliothèque qui résout le cube à votre place.
- Pouvoir expliquer et justifier l'algorithme retenu.

**Approche retenue :** étudier et réimplémenter un algorithme **Two-Phase** documenté, inspiré de Kociemba, sans réutiliser de solveur prêt à l'emploi.

## 2. Architecture générale

```text
$ ./rubik "F R U2 B' L' D'"
             |
             v
+------------------------------------+
| Python — interface                 |
| - arguments et validation          |
| - appel au moteur                  |
| - vérification et sortie           |
+------------------------------------+
             |
             | rubik_core.solve(scramble)
             | liaison pybind11
             v
+------------------------------------+
| C++ — moteur autonome              |
| - représentation du cube           |
| - mouvements et coordonnées        |
| - tables de transitions / pruning  |
| - recherche phase 1 et phase 2     |
| - optimisation                     |
+------------------------------------+
             |
             v
    Séquence de résolution
```

**Principe :** un appel C++ pour une résolution complète, et non un appel Python → C++ à chaque rotation ou nœud exploré. Le moteur C++ doit aussi pouvoir être testé sans Python.

## 3. Arborescence proposée

```text
rubik/
├── rubik                      # Point d'entrée exécutable
├── Makefile
├── pyproject.toml             # Configuration de compilation de l'extension
├── README.md
├── python/
│   ├── main.py                # CLI et affichage
│   ├── parser.py              # Validation de l'entrée
│   ├── verifier.py            # Simulateur indépendant
│   └── benchmark.py           # Mesures de temps et de mouvements
├── cpp/
│   ├── include/
│   │   ├── cube.hpp
│   │   ├── moves.hpp
│   │   ├── coordinates.hpp
│   │   ├── tables.hpp
│   │   └── solver.hpp
│   ├── src/
│   │   ├── cube.cpp
│   │   ├── moves.cpp
│   │   ├── coordinates.cpp
│   │   ├── tables.cpp
│   │   ├── phase1.cpp
│   │   ├── phase2.cpp
│   │   ├── solver.cpp
│   │   └── bindings.cpp
│   └── tests/
│       ├── test_moves.cpp
│       └── test_solver.cpp
├── tests/
│   ├── test_parser.py
│   ├── test_rotations.py
│   ├── test_solutions.py
│   └── test_performance.py
└── data/
    └── pruning_tables/       # Tables générées localement
```

L'arborescence est une proposition de conception, pas une exigence du sujet.

## 4. Répartition des responsabilités

| Python — Personne A | C++ — Personne B |
|---|---|
| Interface CLI et validation | Représentation des 8 coins et 12 arêtes |
| Intégration du module C++ | Rotations, permutations et orientations |
| Simulateur de vérification indépendant | Encodage des états et coordonnées |
| Génération de mélanges et tests | Tables de mouvements et de pruning |
| Benchmarks et mesure HTM | Recherche Two-Phase |
| Vérification du résultat et sortie | Optimisation CPU/mémoire |

**Équilibrage :** la charge de développement C++ est plus importante. La personne Python prend aussi part à la conception mathématique, aux tests de cohérence et à l'analyse des performances.

## 5. Checklist Python

### Infrastructure
- [ ] Créer l'exécutable `rubik` et lire les arguments.
- [ ] Implémenter le parsing de `F R U B L D` avec `'` et `2`.
- [ ] Rejeter les mouvements non autorisés (`M`, `E`, `S`, `x`, `y`, `z`).
- [ ] Intégrer `rubik_core` avec `pybind11`.

### Vérification
- [ ] Développer un simulateur de cube **indépendant** du moteur C++.
- [ ] Vérifier que l'application du mélange puis de la solution résout le cube.
- [ ] Tester les mouvements inverses, doubles et quadruples.
- [ ] Tester les entrées vides, malformées et les espaces multiples.

### Performance et livraison
- [ ] Générer des mélanges reproductibles avec différentes longueurs.
- [ ] Mesurer le nombre de mouvements HTM.
- [ ] Mesurer le temps total de réponse, y compris le chargement éventuel des tables.
- [ ] Tester un ensemble suffisamment varié de mélanges.
- [ ] Garantir que la sortie standard contient uniquement la solution attendue.

## 6. Checklist C++

### Modèle du cube
- [ ] Représenter les 8 coins et les 12 arêtes.
- [ ] Gérer les positions et orientations des pièces.
- [ ] Implémenter les 18 mouvements élémentaires (6 faces × 3 variantes).
- [ ] Tester les invariants du cube et les rotations.

### Recherche
- [ ] Définir les coordonnées d'état de la phase 1.
- [ ] Définir les coordonnées d'état de la phase 2.
- [ ] Générer les tables de transitions.
- [ ] Générer les tables de pruning.
- [ ] Implémenter IDA* ou une recherche adaptée.
- [ ] Implémenter l'enchaînement des deux phases.

### Optimisation et intégration
- [ ] Réduire les allocations et le coût par état exploré.
- [ ] Tester les cas difficiles et mesurer les performances.
- [ ] Exposer `solve(scramble)` via `pybind11`.
- [ ] Documenter l'algorithme, les conventions et la génération des tables.

## 7. Contrat d'interface

L'API publique minimale proposée est :

```python
import rubik_core

solution: str = rubik_core.solve("R U R' U'")
print(solution)
```

**Contrat :**
- Entrée : chaîne de mélange en notation officielle.
- Sortie : chaîne de résolution en notation officielle.
- Erreurs : exceptions Python explicites, converties depuis le C++ si nécessaire.
- Pas d'appels Python ↔ C++ dans la boucle de recherche.
- Convention partagée et documentée pour l'ordre des pièces et leurs orientations.

`pybind11` sert uniquement à l'interopérabilité ; vérifier sa disponibilité dans l'environnement d'évaluation et prévoir une compilation reproductible.

## 8. Ordre de développement

1. **Conventions communes :** notation, ordre des pièces, orientations, erreurs et API.
2. **Simulateurs indépendants :** implémentation des mouvements en Python et en C++, puis comparaison automatique.
3. **Coordonnées et tables :** encodages d'états, transitions, pruning et tests d'invariants.
4. **Solveur Two-Phase :** correction d'abord, puis amélioration de la longueur des solutions et du temps.
5. **Intégration :** exposition du solveur C++ à Python après validation autonome.
6. **Validation finale :** tests massifs, performances, erreurs, installation et démonstration.

## 9. Critères de validation

| Critère | Attendu |
|---|---|
| Correction | Tous les mélanges valides testés doivent être résolus |
| Longueur | Moyenne de **50 mouvements HTM** selon le sujet |
| Délai | **3 secondes maximum** par réponse |
| Notation | `F R U B L D` avec `'` et `2` |
| Méthode | Pas d'inversion directe du mélange |
| Dépendances | Pas de bibliothèque de résolution prête à l'emploi |
| Évaluation | Chaque membre sait expliquer l'algorithme |

## 10. Risques et décisions à prendre tôt

- **Conventions incompatibles :** fixer dès le départ le repérage des faces, des pièces et des orientations.
- **Erreurs difficiles à diagnostiquer :** maintenir un simulateur Python indépendant pour comparer les mouvements et les solutions.
- **Tables volumineuses :** documenter leur génération, leur format et leur chargement.
- **Dépassement des 3 secondes :** mesurer le temps de bout en bout, pas uniquement la recherche C++.
- **Dépendance de compilation :** tester le lancement depuis un environnement propre et sur la VM prévue pour l'évaluation.
- **Charge inégale :** partager la conception de l'algorithme et réserver à Python une vraie responsabilité de validation.

## 11. Décision finale

**Architecture retenue :** Python pour l'interface, les tests et la validation ; C++ pour le moteur complet ; `pybind11` comme liaison ; conception mathématique commune. C'est une architecture simple à tester, qui évite les échanges fréquents entre langages pendant la recherche.

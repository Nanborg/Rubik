# Renderer — nicolsan

## Objectif

Un cube 3D lisible et agréable qui montre les mouvements envoyés par le solver,
permet de les rejouer et aide à repérer une mauvaise rotation ou une erreur de
résolution. La visualisation est un bonus du sujet et un outil pour travailler
à deux ; la résolution reste utilisable seule.

## Parcours prévu

1. Charger le mélange initial ou un état cubie JSON valide.
2. Lire les mouvements sur stdin et les valider avant de commencer.
3. Montrer l'état initial avec les couleurs du contrat.
4. Lire automatiquement ou avancer mouvement par mouvement.
5. Afficher l'état final et indiquer s'il est résolu.

## Éléments visuels

- Cubies sombres, stickers bien séparés, six couleurs constantes.
- Éclairage doux et relief lisible, sans masquer les stickers.
- Caméra orbitale et zoom ; bouton de retour à la vue initiale.
- Mouvement courant mis en évidence dans la séquence.
- Flèche ou surbrillance sur la couche qui va tourner.
- Lecture/pause, pas suivant/précédent, recommencer.
- Vitesse et délai initial réglables.
- État initial/final, compteur de mouvements et résultat de vérification.

Les indications d'étapes CFOP sont un enrichissement ultérieur : la ligne de
mouvements seule ne fournit pas leurs frontières. Les obtenir par des
métadonnées séparées, jamais en polluant stdout du solver.

## Ordre de réalisation

Commencer par le mode logs et les états de référence, puis un cube statique,
un quart de tour, toutes les faces, la lecture complète et enfin les contrôles
et finitions visuelles. Ne pas attendre la fin du solver : utiliser des listes
de mouvements et états attendus écrits à la main.

## Contraintes techniques

Respecter docs/CONVENTIONS.md pour axes, sens, couleurs et positions.
La caméra ne change jamais la signification de F ou U.
L'état logique est discret ; l'interpolation visuelle n'est pas l'état du cube.
Un retour en arrière restaure un état connu ou applique un inverse exact.
La bibliothèque 3D reste à choisir et à justifier ; elle sera optionnelle
pour le solver et les tests sans affichage.

## Tests à prévoir

Chaque face en quart/demi-tour/inverse ; plusieurs rotations successives ;
pause et reprise au milieu d'une animation ; changement de vitesse ;
retour au début et au mouvement précédent ; entrée vide ; token invalide ;
état impossible ; fin de fichier ; fermeture de fenêtre ; solution qui ne
résout pas. Comparer les stickers attendus, pas seulement une impression visuelle.

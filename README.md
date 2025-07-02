# 🔗 Projet Spark — Amis Communs

Ce projet met en œuvre un algorithme distribué avec Apache Spark pour identifier les **amis communs** entre chaque paire d’utilisateurs d’un réseau social. Il utilise deux implémentations : en Scala et en Python (PySpark).

---

##  Contenu du projet

- `MutualFriends.scala` : implémentation Spark avec Scala
- `mutual_friends_args.py` : implémentation PySpark prenant des arguments (exécution flexible)
- `amis_communs.csv`, `social_graph.txt`, `soc-LiveJournal1Adj.txt` : fichiers d’entrée représentant des graphes sociaux
- `run_all.bat`, `launch_interactive.bat` : scripts Windows pour faciliter l'exécution
- `TP Spark – Rapport complet.pdf` : document PDF décrivant l’algorithme, les résultats, et la méthodologie

---

##  Objectif du Projet

Trouver pour chaque **paire d’utilisateurs** d’un réseau social leurs **amis communs**. Ce problème est typique des traitements de graphes distribués et permet de mettre en pratique les opérations de jointure, de transformation et d’agrégation dans Spark.

---

##  Format des Fichiers d’Entrée

Les fichiers doivent contenir les relations d’amitié sous le format :

```
utilisateur1 ami1,ami2,ami3,...
```

Exemple :
```
1 2,3,4
2 1,4
3 1,4
```

Ici :
- L'utilisateur 1 est ami avec 2, 3, 4
- L'utilisateur 2 est ami avec 1, 4
- L'utilisateur 3 est ami avec 1, 4

---

##  Principe de l’Algorithme

1. Lire les relations d’amitié.
2. Pour chaque utilisateur, générer toutes les paires possibles avec ses amis.
3. Associer à chaque paire la liste des amis.
4. Regrouper par paire et faire l'intersection des listes d’amis pour trouver les amis communs.

---

##  Format de Sortie Attendu

Exemple :
```
(1,2) -> [4]
(1,3) -> [4]
(2,3) -> [1,4]
```

Chaque ligne représente une **paire d’amis** et leurs **amis en commun**.

---

##  Exécution

###  En Python (PySpark)
Assurez-vous d’avoir installé Spark et Python. Puis exécutez :

```bash
spark-submit mutual_friends_args.py input/social_graph.txt output/
```

Vous pouvez remplacer `input/social_graph.txt` par tout autre fichier d'entrée.

###  En Scala
Compiler le fichier avec `sbt`, puis :

```bash
spark-submit --class MutualFriends path/to/MutualFriends.jar input/social_graph.txt output/
```

---

##  Dépendances Techniques

- Apache Spark ≥ 2.4
- Java ≥ 8
- Python ≥ 3.6 (pour la version PySpark)
- Scala ≥ 2.11 (pour la version Scala)
- sbt (pour compiler le code Scala si besoin)

---

##  Rapport

Le fichier `TP Spark – Rapport complet _ Amis en commun.pdf` contient :
- Présentation du problème
- Étapes de l’algorithme
- Explication du code Python et Scala
- Tests sur différents jeux de données
- Capture d’écran des résultats
- Conclusion

---

##  Auteur

Projet réalisé par **Mohamed Mahmoud Ahmedou Beffa**  dans le cadre d’un Projet sur Apache Spark et les systèmes distribués.
 Voici mon Mail Gmail : tijanibeffa@gmail.com pour reppondre a Votre questions

---

##  Remarques

- Le programme fonctionne avec des données simulées (amis_communs.csv) ou réelles (soc-LiveJournal1Adj.txt).
- Bien respecter le format des fichiers d’entrée.
- Pour de très grands fichiers, privilégiez l’exécution sur un cluster Spark (ou Google Colab + PySpark).

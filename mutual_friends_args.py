from pyspark import SparkContext
import sys
import csv

sc = SparkContext("local", "MutualFriendsArgs")
sc.setLogLevel("ERROR")

# 📥 Lecture du fichier d'entrée
lines = sc.textFile("C:/spark/projects/social_graph.txt")

# 🧩 Parsing des lignes
def parse_line(line):
    parts = line.strip().split()
    user_id = parts[0]
    name = parts[1]
    friends = parts[2].split(",") if len(parts) > 2 else []
    return (user_id, name, friends)

parsed = lines.map(parse_line)

# 🗺️ Dictionnaire {ID: Nom}
id_to_name = parsed.map(lambda x: (x[0], x[1])).collectAsMap()

# 🔄 Génération des paires (min, max)
def generate_pairs(x):
    user_id, _, friends = x
    pairs = []
    for friend in friends:
        pair = tuple(sorted([user_id, friend]))
        pairs.append((pair, set(friends)))
    return pairs

pairs = parsed.flatMap(generate_pairs)

# 👯 Calcul des amis en commun
mutuals = pairs.reduceByKey(lambda a, b: a.intersection(b))

# ✅ Partie 1 : afficher les amis communs pour 2 IDs donnés
if len(sys.argv) == 3:
    id1, id2 = sorted([sys.argv[1], sys.argv[2]])
    name1 = id_to_name.get(id1, f"User_{id1}")
    name2 = id_to_name.get(id2, f"User_{id2}")
    result = mutuals.filter(lambda x: x[0] == (id1, id2)).collect()
    if result:
        mutual_ids = result[0][1]
        mutual_names = [id_to_name.get(fid, f"User_{fid}") for fid in mutual_ids]
        print(f"\n>>> {id1}<{name1}> et {id2}<{name2}> ont en commun : [{', '.join(mutual_names)}]")
    else:
        print(f"\n Aucun ami commun entre {id1} et {id2}")

# 📄 Partie 2 : Export de toutes les paires avec amis communs vers CSV
all_results = mutuals.collect()
with open("amis_communs.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Utilisateur1", "Utilisateur2", "AmisCommuns"])
    for ((u1, u2), common_ids) in all_results:
        name1 = id_to_name.get(u1, f"User_{u1}")
        name2 = id_to_name.get(u2, f"User_{u2}")
        common_names = [id_to_name.get(fid, f"User_{fid}") for fid in common_ids]
        writer.writerow([f"{u1}<{name1}>", f"{u2}<{name2}>", ", ".join(common_names)])

print("\n Fichier CSV généré : amis_communs.csv")

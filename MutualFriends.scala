// Lire les arguments : chemin du fichier + seuil minimum
val args = spark.conf.get("spark.driver.args").split(" ")
val inputFile = args(0)
val minCommon = args(1).toInt

println(s">>> Fichier: $inputFile")
println(s">>> Seuil minimum d'amis en commun: $minCommon")

// Lire les données
val data = sc.textFile(inputFile)
val data1 = data.map(x => x.split("\t")).filter(li => li.length == 2)

// Générer les paires (user1, user2) et liste d’amis
def pairs(str: Array[String]) = {
  val users = str(1).split(",")
  val user = str(0)
  for (i <- 0 until users.length) yield {
    val pair = if (user < users(i)) (user, users(i)) else (users(i), user)
    (pair, users)
  }
}

val pairCounts = data1.flatMap(pairs).reduceByKey((a, b) => a.intersect(b))
val results = pairCounts.map {
  case ((u1, u2), friends) => s"$u1\t$u2\t${friends.mkString(",")}"
}

// Afficher les 10 premières lignes
println("\n----- Résultats bruts (10 lignes) -----")
results.take(10).foreach(println)

// Filtrer par nombre minimum d'amis en commun
val filtered = results.filter(line => line.split("\t")(2).split(",").count(_.nonEmpty) >= minCommon)

println(s"\n----- Résultats filtrés (>= $minCommon amis en commun) -----")
filtered.take(10).foreach(println)

// Sauvegarde texte classique
val outputPath = s"C:/spark/projects/output_min$minCommon"
filtered.saveAsTextFile(outputPath)
println(s"\n✅ Résultats filtrés enregistrés dans : $outputPath")

// Générer un CSV
val csvHeader = "userA,userB,mutual_friends,nb_mutuals"
val csvData = filtered.map { line =>
  val parts = line.split("\t")
  val userA = parts(0)
  val userB = parts(1)
  val mutuals = parts(2)
  val count = if (mutuals.nonEmpty) mutuals.split(",").count(_.nonEmpty) else 0
  s"""$userA,$userB,"$mutuals",$count"""
}

val csvFull = sc.parallelize(Seq(csvHeader)) ++ csvData
val csvPath = s"C:/spark/projects/output_csv_min$minCommon"
csvFull.saveAsTextFile(csvPath)
println(s"\n📄 CSV généré dans : $csvPath")

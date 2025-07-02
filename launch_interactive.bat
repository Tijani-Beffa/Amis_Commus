@echo off
set /p ID1=Entrez l'ID du premier utilisateur :
set /p ID2=Entrez l'ID du deuxieme utilisateur :

echo.
echo 🔄 Lancement de Spark avec les IDs %ID1% et %ID2% ...
set PYSPARK_PYTHON=C:\Program Files\Python311\python.exe
spark-submit mutual_friends_args.py %ID1% %ID2%

pause

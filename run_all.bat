@echo off
setlocal

:: === Paramètres attendus : fichier.txt + seuil
IF "%~1"=="" (
    echo  Fichier d'entrée manquant.
    echo Usage : run_all.bat fichier.txt min_amis
    goto end
)

IF "%~2"=="" (
    echo  Seuil minimum d'amis communs manquant.
    echo Usage : run_all.bat fichier.txt min_amis
    goto end
)

:: === Définir chemins
set FILE_PATH=C:\spark\projects\%~1
set MIN_AMIS=%~2
set SCALA_FILE=C:\spark\projects\MutualFriends.scala
set OUT_TXT=C:\spark\projects\output_min%MIN_AMIS%
set OUT_CSV=C:\spark\projects\output_csv_min%MIN_AMIS%
set FINAL_CSV=%OUT_CSV%\results.csv

:: === Vérification du fichier d’entrée
IF NOT EXIST "%FILE_PATH%" (
    echo  Le fichier "%FILE_PATH%" n'existe pas !
    goto end
)

:: === Supprimer anciens résultats
rmdir /S /Q "%OUT_TXT%" 2>nul
rmdir /S /Q "%OUT_CSV%" 2>nul
del /Q "%FINAL_CSV%" 2>nul

echo ==============================================
echo   Lancement de Spark avec MutualFriends.scala
echo   Fichier : %FILE_PATH%
echo   Seuil d'amis en commun : %MIN_AMIS%
echo ==============================================

:: === Exécuter le programme Spark
spark-shell --conf spark.driver.args="%FILE_PATH% %MIN_AMIS%" -i "%SCALA_FILE%"

:: === Fusionner les fichiers CSV Spark dans un seul fichier
echo.
echo  Fusion des fichiers CSV (part-*) en : results.csv

:: Vérifie si le dossier CSV existe
IF EXIST "%OUT_CSV%" (
    (
        for %%f in (%OUT_CSV%\part-*) do (
            type "%%f"
        )
    ) > "%FINAL_CSV%"
    echo  CSV fusionné : %FINAL_CSV%
) ELSE (
    echo  Dossier %OUT_CSV% introuvable. Rien à fusionner.
)

:end
pause

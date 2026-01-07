import PyInstaller.__main__
import os

# Nom de votre script principal (Changez-le si votre fichier ne s'appelle pas main.py)
SCRIPT_PRINCIPAL = "main.py"

# Nom de votre image (Doit être dans le même dossier)
IMAGE_FOND = "parchemin.jpg"

# Nom de l'icône (Optionnel, mettez None si vous n'en avez pas)
ICONE = None  # Exemple : "mon_icone.ico"

print("--- DÉBUT DE LA COMPILATION ---")

# Définition des arguments pour PyInstaller
args = [
    SCRIPT_PRINCIPAL,
    '--onefile',            # Un seul fichier .exe
    '--noconsole',          # Pas de fenêtre noire (console)
    '--name=FeuilleAventure', # Nom du fichier final
    '--clean',              # Nettoyer les caches avant de compiler
]

# Gestion de l'ajout de l'image (le séparateur change selon Windows ou Mac/Linux)
if os.name == 'nt': # Si Windows
    args.append(f'--add-data={IMAGE_FOND};.')
else: # Si Mac ou Linux
    args.append(f'--add-data={IMAGE_FOND}:.')

# Ajout de l'icône si elle existe
if ICONE and os.path.exists(ICONE):
    args.append(f'--icon={ICONE}')

# Lancement de la compilation
PyInstaller.__main__.run(args)

print(f"--- TERMINE ! Vérifiez le dossier 'dist' ---")

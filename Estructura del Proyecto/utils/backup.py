import os
import shutil
from datetime import datetime

def backup_db(ruta_db="database/parking.db", carpeta_backup="backups"):
    """
    Crea una copia de seguridad de la base de datos SQLite.
    Guarda el archivo con un timestamp en la carpeta indicada.
    """
    # Crea la carpeta de backups si no existe
    os.makedirs(carpeta_backup, exist_ok=True)

    # Define el nombre del archivo destino con fecha y hora
    destino = f"{carpeta_backup}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

    # Copia el archivo de base de datos
    shutil.copy2(ruta_db, destino)

    return destino


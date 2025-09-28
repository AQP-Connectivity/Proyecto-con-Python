import shutil
from datetime import datetime

def backup_db(ruta_db="database/parking.db", carpeta_backup="backups"):
  os.makedirs(carpeta_backup, exist_ok=True)
  destino = f"{carpeta_backup}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2(ruta_db, destino)
return destino

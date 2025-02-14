import os
import shutil
import csv
from datetime import datetime
import locale

# Establecer el idioma a español para los nombres de los meses
locale.setlocale(locale.LC_TIME, "es_ES.utf8")  # En algunos sistemas puede ser "Spanish_Spain.1252"

# Ruta de la carpeta donde están los archivos
source_folder = r"Z:"
destination_folder = source_folder  # Se mantendrá dentro de 'horas'

# Verificar si la carpeta existe
if not os.path.exists(source_folder):
    print("La carpeta de origen no existe.")
    exit()

# Procesar archivos en la carpeta
for filename in os.listdir(source_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(source_folder, filename)

        try:
            # Leer el archivo y obtener la fecha relevante
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                first_row = next(reader, None)  # Leer primera fila

            if first_row:
                date_str = first_row[4].split()[0]  # Extraer fecha (dd/mm/yyyy)
                date_obj = datetime.strptime(date_str, "%d/%m/%Y")

                # Obtener el mes en español
                month_name = date_obj.strftime("%B").capitalize()  # Nombre del mes con la primera letra en mayúscula

                # Construir carpetas de destino
                year_folder = os.path.join(destination_folder, str(date_obj.year))
                month_folder = os.path.join(year_folder, month_name)

                # Crear carpetas si no existen
                os.makedirs(month_folder, exist_ok=True)

                # Mover el archivo
                shutil.move(file_path, os.path.join(month_folder, filename))
                print(f"Movido: {filename} → {month_folder}")

        except PermissionError:
            print(f"⚠️ No se pudo mover {filename}: Está abierto en otro programa.")
        except Exception as e:
            print(f"❌ Error con {filename}: {e}")

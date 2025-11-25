from rembg import remove
from PIL import Image
import os

print("=== Remove Background Utility ===")
print("Arrastra una imagen aquí y presiona ENTER:")

#* El usuario arrastra la imagen → Windows pega la ruta absoluta → input() la captura
path_img = input().strip().replace('"', '').replace("'", "")

if not os.path.exists(path_img):
    raise FileNotFoundError(f"No existe la imagen en: {path_img}")

#* Obtenemos nombre y carpeta original
folder = os.path.dirname(path_img)
filename = os.path.basename(path_img)
name_without_ext = os.path.splitext(filename)[0]

#* Construimos ruta de salida en la misma carpeta
output_path = os.path.join(folder, f"{name_without_ext}_no_bg.png")

#* Procesar imagen
input_img = Image.open(path_img)
output = remove(input_img)
output.save(output_path)  # type: ignore

print(f"¡Imagen procesada exitosamente!")
print(f"Se guardó en: {output_path}")

from rembg import remove
from PIL import Image
import os

#TODO Usar ruta absoluta para evitar
path_img = 'C:/Users/JuanferDev/Desktop/Utilities-Python/RemoveBackground/img_test.jpg'
output_path = "C:/Users/JuanferDev/Desktop/Utilities-Python/RemoveBackground/img_test_sin_fondo.png"

if not os.path.exists(path_img):
    raise FileNotFoundError(f"No existe la imagen en: {path_img}")

input_img = Image.open(path_img)

output = remove(input_img)
output.save(output_path) # type: ignore

print("¡Imagen procesada y guardada en:", output_path)

"""
image_compressor.py
Compresor simple de imágenes (JPEG/PNG/WebP).
- Acepta ruta de archivo o arrastrar+enter en consola.
- Ajusta quality (JPEG) o compress_level (PNG).
- Opcional: redimensionar manteniendo aspect ratio.
- Guarda como <original>_compressed.<ext> en la misma carpeta.
"""

import os
import argparse
from PIL import Image

SUPPORTED_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff")
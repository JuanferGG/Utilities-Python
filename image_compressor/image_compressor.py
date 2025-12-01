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


def compress_image(input_path: str, quality: int = 85, png_level: int = 6,
                   max_size: int | None = None, output_path: str | None = None, to_format: str | None = None):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No existe la imagen en: {input_path}")

    base_dir = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    ext_lower = ext.lower()

    if to_format:
        out_ext = f".{to_format.lower().lstrip('.')}"
    else:
        out_ext = ext_lower

    if output_path:
        out_path = output_path
    else:
        out_filename = f"{name}_compressed{out_ext}"
        out_path = os.path.join(base_dir, out_filename)

    img = Image.open(input_path)

    if max_size:
        img.thumbnail((max_size, max_size))

    save_kwargs = {}
    if out_ext in (".jpg", ".jpeg"):
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert("RGB")
        save_kwargs["quality"] = int(max(10, min(95, quality)))
        save_kwargs["optimize"] = True

    elif out_ext == ".png":
        save_kwargs["optimize"] = True
        save_kwargs["compress_level"] = int(max(0, min(9, png_level)))

    elif out_ext == ".webp":
        save_kwargs["quality"] = int(max(10, min(95, quality)))
        save_kwargs["method"] = 6

    else:
        pass

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    img.save(out_path, **save_kwargs)

    original_size = os.path.getsize(input_path)
    new_size = os.path.getsize(out_path)

    return out_path, original_size, new_size


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def main():
    parser = argparse.ArgumentParser(prog="image_compressor",
                                     description="Compress a single image and save next to original with _compressed suffix.")
    parser.add_argument("path", nargs="?", help="Path to image. If omitted, you can drag & drop path into console when prompted.")
    parser.add_argument("-q", "--quality", type=int, default=85, help="Quality for JPEG/WEBP (10-95). Default: 85")
    parser.add_argument("--png-level", type=int, default=6, help="PNG compress level 0-9 (default 6)")
    parser.add_argument("--max-size", type=int, default=None, help="Max width/height in px (keeps aspect ratio).")
    parser.add_argument("-o", "--output", default=None, help="Explicit output path. If omitted, saved next to original with _compressed suffix.")
    parser.add_argument("--to-format", choices=["jpg", "jpeg", "png", "webp"], help="Force output format (e.g. jpg).")
    args = parser.parse_args()

    path = args.path
    if not path:
        print("Arrastra el archivo aquí (o escribe la ruta) y presiona ENTER:")
        path = input().strip().replace('"', "").replace("'", "")

    if not os.path.exists(path):
        path = os.path.expanduser(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"No existe la imagen en: {path}")

    _, ext = os.path.splitext(path)
    if ext.lower() not in SUPPORTED_EXT:
        print("Advertencia: formato no soportado o no común:", ext)

    out_path, orig_size, new_size = compress_image(path, quality=args.quality, png_level=args.png_level,
                                                   max_size=args.max_size, output_path=args.output, to_format=args.to_format)

    print("\nResultado:")
    print(" Input :", path)
    print(" Output:", out_path)
    print(f" Tamaño original: {human_size(orig_size)} -> Nuevo tamaño: {human_size(new_size)}")
    saved = orig_size - new_size
    pct = (saved / orig_size * 100) if orig_size else 0
    print(f" Ahorro: {human_size(saved)} ({pct:.1f}%)")


if __name__ == "__main__":
    main()

from PIL import Image, ExifTags
from pathlib import Path

def read_exif(image_path):
    image_path = Path(image_path)
    info = {}
    try:
        with Image.open(image_path) as img:
            exif = img.getexif()
            if exif:
                for k, v in exif.items():
                    tag = ExifTags.TAGS.get(k, str(k))
                    if isinstance(v, bytes):
                        try:
                            v = v.decode('utf-8', errors='ignore')
                        except Exception:
                            v = str(v)
                    info[tag] = v
    except Exception as e:
        info['error'] = str(e)
    return info

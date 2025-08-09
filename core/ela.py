from PIL import Image, ImageChops, ImageStat
from pathlib import Path

def ela_analyze(image_path, quality=95, save_dir=Path('output')):
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    image_path = Path(image_path)

    with Image.open(image_path).convert('RGB') as im:
        tmp_jpeg = save_dir / (image_path.stem + '_tmp_ela.jpg')
        im.save(tmp_jpeg, 'JPEG', quality=quality)
        with Image.open(tmp_jpeg) as im2:
            ela = ImageChops.difference(im, im2)
            extrema = ela.getextrema()
            max_diff = max([e[1] for e in extrema]) or 1
            scale = 255.0 / max_diff
            ela = ImageChops.multiply(ela, Image.new('RGB', ela.size, (int(scale), int(scale), int(scale))))
            stat = ImageStat.Stat(ela)
            mean_intensity = sum(stat.mean)/3.0
            ela_path = save_dir / (image_path.stem + '_ELA.png')
            ela.save(ela_path)
    # Normalize score to 0-100
    ela_score = max(0.0, min(100.0, (mean_intensity / 255.0) * 100.0))
    return {'ela_score': round(ela_score, 2), 'ela_image_path': str(ela_path)}

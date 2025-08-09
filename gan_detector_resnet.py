from pathlib import Path

def load_model(model_path=Path('models/gan_detector_resnet.h5')):
    model_path = Path(model_path)
    if not model_path.exists():
        return None, 'Model bulunamadı, GAN tespiti pasif.'
    try:
        from tensorflow.keras.models import load_model as _load
        model = _load(model_path)
        return model, None
    except Exception as e:
        return None, f'Model yüklenemedi: {e}'

def score_image(model, image_path):
    if model is None:
        return {'gan_score': None, 'note': 'Model yok'}
    return {'gan_score': None, 'note': 'Model yüklü ama skorlama uygulanmadı (şablon).'}

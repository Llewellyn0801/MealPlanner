from pathlib import Path

STATIC_IMAGES_DIR = Path(__file__).resolve().parents[1] / "static" / "images"
ALLOWED_IMAGE_EXTENSIONS = {".gif", ".jpeg", ".jpg", ".png", ".webp"}


def safe_image_filename(filename: str) -> str:
    candidate = Path(filename).name.strip().replace(" ", "-").lower()
    suffix = Path(candidate).suffix
    if not candidate or suffix not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Unsupported image filename")
    return candidate


def is_available_local_image(image_url: str | None) -> bool:
    if not image_url or not image_url.startswith("/static/images/"):
        return True

    relative_path = image_url.removeprefix("/static/images/")
    image_path = (STATIC_IMAGES_DIR / relative_path).resolve()
    try:
        image_path.relative_to(STATIC_IMAGES_DIR.resolve())
    except ValueError:
        return False
    return image_path.is_file()

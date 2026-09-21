from pathlib import Path

import pytest

from meal_planner.database.seed import SEED_MEALS
from meal_planner.services.images import is_available_local_image, safe_image_filename

IMAGE_DIR = (
    Path(__file__).resolve().parents[1] / "src" / "meal_planner" / "static" / "images"
)


def test_all_seeded_local_images_exist():
    image_urls = {
        meal["image_url"]
        for meal in SEED_MEALS
        if isinstance(meal.get("image_url"), str)
        and meal["image_url"].startswith("/static/images/")
    }

    assert image_urls
    assert all(
        (IMAGE_DIR / image_url.removeprefix("/static/images/")).is_file()
        for image_url in image_urls
    )


def test_shrimp_zucchini_salad_does_not_use_the_curry_image():
    shrimp_salad = next(
        meal
        for meal in SEED_MEALS
        if meal["name"] == "Mediterranean Grilled Shrimp & Zucchini Salad"
    )

    assert shrimp_salad["image_url"] is None


def test_verified_recipe_images_match_the_recipe():
    names_without_verified_images = {
        "Rosemary Chicken Thighs & Roasted Brussels Sprouts",
    }
    meals = {meal["name"]: meal for meal in SEED_MEALS}

    assert all(
        meals[name]["image_url"] is None for name in names_without_verified_images
    )
    assert meals["Pan-Seared Salmon & Quinoa Grain Bowl"]["image_url"].endswith(
        "salmon-quinoa-grain-bowl.jpg"
    )
    assert meals["Grass-Fed Sirloin Steak & Sauteed Green Beans"]["image_url"].endswith(
        "grass-fed-sirloin-steak-sauteed-green-beans.jpg"
    )
    assert meals["Grilled Chicken Shawarma & Herb Tahini Bowl"]["image_url"].endswith(
        "chicken-shawarma-tahini-platter.jpg"
    )


def test_chinese_beef_uses_verified_beef_broccoli_image():
    chinese_beef = next(
        meal
        for meal in SEED_MEALS
        if meal["name"] == "Chinese Beef & Broccoli with Garlic"
    )

    assert chinese_beef["image_url"] == "/static/images/asian-beef-broccoli-skillet.jpg"


def test_local_image_validation_rejects_missing_and_traversal_paths():
    assert is_available_local_image("/static/images/greek-yogurt-berry-&-chia-bowl.png")
    assert not is_available_local_image("/static/images/does-not-exist.jpg")
    assert not is_available_local_image("/static/images/../seed.py")


def test_safe_image_filename_rejects_unsafe_extensions():
    assert safe_image_filename("My Dish.JPG") == "my-dish.jpg"
    with pytest.raises(ValueError):
        safe_image_filename("../../meal_planner.py")

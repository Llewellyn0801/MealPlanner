from fastapi.testclient import TestClient

from meal_planner.main import app

client = TestClient(app)


def test_recipe_and_pantry_routes_are_registered():
    assert client.get("/recipes/manage").status_code == 200
    assert client.get("/pantry/").status_code == 200

from fastapi.testclient import TestClient

from meal_planner.database.session import SessionLocal
from meal_planner.main import app
from meal_planner.models.meal import Household, HouseholdMember


def test_recipe_and_pantry_routes_are_registered():
    with TestClient(app) as client:
        assert client.get("/recipes/manage").status_code == 200
        assert client.get("/recipes/image-audit").status_code == 200
        assert client.get("/pantry/").status_code == 200


def test_default_household_profiles_are_available_and_selectable():
    with TestClient(app) as client:
        response = client.get("/profile")
        assert response.status_code == 200
        assert response.headers["cache-control"] == "no-store, no-cache, must-revalidate"
        assert "Naickers household" in response.text
        assert all(name in response.text for name in [
            "Llewellyn",
            "Esmerelda",
            "Sebastian",
            "Tristan",
            "Quen",
        ])

        db = SessionLocal()
        try:
            member = (
                db.query(HouseholdMember)
                .join(Household, Household.id == HouseholdMember.household_id)
                .filter(Household.name == "Naickers", HouseholdMember.name == "Llewellyn")
                .first()
            )
            assert member is not None
            selection = client.post(f"/profile/select/{member.id}", follow_redirects=False)
            assert selection.status_code == 303
            assert selection.headers["location"] == "/"
            assert "meal_planner_member_id" in selection.headers["set-cookie"]

            saved = client.post(
                f"/profile/member/{member.id}",
                data={
                    "profile": "higher_protein",
                    "household_size": "1",
                    "activity_level": "high",
                    "maintenance_calories": "3000",
                    "target_calories": "2800",
                    "macro_focus": "protein",
                },
                follow_redirects=False,
            )
            assert saved.status_code == 303
            db.refresh(member)
            assert member.profile == "higher_protein"
            assert member.activity_level == "high"
            assert member.target_calories == 2800
        finally:
            db.close()

from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from meal_planner.database.session import get_db
from meal_planner.models.meal import Household, HouseholdMember

router = APIRouter(prefix="/profile")
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parents[1] / "templates")
)
PROFILE_COOKIE = "meal_planner_member_id"
DEFAULT_HOUSEHOLD = "Naickers"
DEFAULT_MEMBERS = ["Llewellyn", "Esmerelda", "Sebastian", "Tristan", "Quen"]


def get_or_create_default_household(db: Session) -> Household:
    household = db.query(Household).filter(Household.name == DEFAULT_HOUSEHOLD).first()
    if not household:
        household = Household(name=DEFAULT_HOUSEHOLD)
        db.add(household)
        db.flush()

    existing_names = {
        member.name for member in db.query(HouseholdMember).filter(
            HouseholdMember.household_id == household.id
        )
    }
    for name in DEFAULT_MEMBERS:
        if name not in existing_names:
            db.add(
                HouseholdMember(
                    household_id=household.id,
                    name=name,
                    role="owner" if name == "Llewellyn" else "member",
                )
            )
    db.commit()
    return household


@router.get("", response_class=HTMLResponse)
def profile_page(request: Request, db: Session = Depends(get_db)):
    household = get_or_create_default_household(db)
    members = (
        db.query(HouseholdMember)
        .filter(HouseholdMember.household_id == household.id)
        .order_by(HouseholdMember.id)
        .all()
    )
    selected_id = request.cookies.get(PROFILE_COOKIE)
    selected_member = next(
        (member for member in members if str(member.id) == selected_id), None
    )
    response = templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "request": request,
            "household": household,
            "members": members,
            "selected_member": selected_member,
        },
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response


@router.post("/household")
def create_household(
    household_name: str = Form(...),
    member_names: str = Form(...),
    db: Session = Depends(get_db),
):
    name = household_name.strip()
    names = [item.strip() for item in member_names.split(",") if item.strip()]
    if not name or not names:
        return RedirectResponse(url="/profile", status_code=303)

    household = db.query(Household).filter(Household.name == name).first()
    if not household:
        household = Household(name=name)
        db.add(household)
        db.flush()
    existing_names = {
        member.name.lower()
        for member in db.query(HouseholdMember).filter(
            HouseholdMember.household_id == household.id
        )
    }
    for member_name in names:
        if member_name.lower() not in existing_names:
            db.add(HouseholdMember(household_id=household.id, name=member_name))
    db.commit()
    return RedirectResponse(url="/profile", status_code=303)


@router.post("/select/{member_id}")
def select_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(HouseholdMember).filter(HouseholdMember.id == member_id).first()
    if not member:
        return RedirectResponse(url="/profile", status_code=303)
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(PROFILE_COOKIE, str(member.id), httponly=True, samesite="lax")
    return response


@router.post("/member/{member_id}")
def update_member_profile(
    member_id: int,
    profile: str = Form("general"),
    household_size: int = Form(1),
    activity_level: str = Form("sedentary"),
    maintenance_calories: int | None = Form(None),
    target_calories: int | None = Form(None),
    macro_focus: str = Form("balanced"),
    db: Session = Depends(get_db),
):
    member = db.query(HouseholdMember).filter(HouseholdMember.id == member_id).first()
    if not member:
        return RedirectResponse(url="/profile", status_code=303)
    member.profile = profile.strip()
    member.household_size = max(1, household_size)
    member.activity_level = activity_level.strip()
    member.maintenance_calories = maintenance_calories
    member.target_calories = target_calories
    member.macro_focus = macro_focus.strip()
    db.commit()
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(PROFILE_COOKIE, str(member.id), httponly=True, samesite="lax")
    return response

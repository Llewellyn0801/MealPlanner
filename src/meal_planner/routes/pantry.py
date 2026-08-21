from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from meal_planner.database.session import get_db
from meal_planner.models.meal import PantryItem
from meal_planner.services.grocery import categorize_ingredient

router = APIRouter(prefix="/pantry")


@router.get("/")
def get_pantry_items(db: Session = Depends(get_db)):
    items = db.query(PantryItem).order_by(PantryItem.category, PantryItem.name).all()
    return [
        {
            "id": i.id,
            "name": i.name,
            "category": i.category,
            "is_in_stock": i.is_in_stock,
        }
        for i in items
    ]


@router.post("/add")
def add_pantry_item(
    payload: dict[str, Any] = Body(...), db: Session = Depends(get_db)
):
    name = str(payload.get("name", "")).strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")

    category = payload.get("category") or categorize_ingredient(name)
    is_in_stock = bool(payload.get("is_in_stock", True))

    existing = db.query(PantryItem).filter(PantryItem.name.ilike(name)).first()
    if existing:
        existing.is_in_stock = is_in_stock
        db.commit()
        return {"id": existing.id, "name": existing.name, "is_in_stock": existing.is_in_stock}

    item = PantryItem(name=name, category=category, is_in_stock=is_in_stock)
    db.add(item)
    db.commit()
    return {"id": item.id, "name": item.name, "category": item.category, "is_in_stock": item.is_in_stock}


@router.post("/toggle")
def toggle_pantry_item(
    payload: dict[str, Any] = Body(...), db: Session = Depends(get_db)
):
    item_id = payload.get("id")
    name = payload.get("name")

    item = None
    if item_id:
        item = db.query(PantryItem).filter(PantryItem.id == item_id).first()
    elif name:
        item = db.query(PantryItem).filter(PantryItem.name.ilike(str(name).strip())).first()

    if not item and name:
        category = categorize_ingredient(str(name))
        item = PantryItem(name=str(name).strip(), category=category, is_in_stock=True)
        db.add(item)
        db.commit()
        return {"id": item.id, "name": item.name, "is_in_stock": item.is_in_stock}

    if not item:
        raise HTTPException(status_code=404, detail="Pantry item not found")

    item.is_in_stock = not item.is_in_stock
    db.commit()
    return {"id": item.id, "name": item.name, "is_in_stock": item.is_in_stock}


@router.post("/delete")
def delete_pantry_item(
    payload: dict[str, Any] = Body(...), db: Session = Depends(get_db)
):
    item_id = payload.get("id")
    item = db.query(PantryItem).filter(PantryItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return {"success": True}

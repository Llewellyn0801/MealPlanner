import json

from sqlalchemy.orm import Session

from meal_planner.database.session import SessionLocal
from meal_planner.models.meal import Meal

SEED_MEALS = [
    {
        "name": "Ground Beef & Eggs Bowl",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Savory, high-protein breakfast bowl ready in under 15 minutes.",
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
        "ingredients": [
            "200g ground beef",
            "2 large eggs",
            "1 tsp butter",
            "1/4 tsp sea salt",
        ],
        "instructions": [
            "Heat a skillet over medium heat and melt the butter.",
            "Add ground beef, season with salt and pepper, and cook until browned.",
            "Push beef to one side, crack in eggs, and scramble until just set.",
            "Mix eggs with beef and serve warm.",
        ],
        "cooking_tips": "Do not overcook the eggs; remove from heat while still soft.",
        "tags": "carnivore,low_carb,high_protein,kid_friendly",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Greek Yogurt Berry Bowl",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Creamy, refreshing bowl with fiber and protein.",
        "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777",
        "ingredients": [
            "1 cup plain Greek yogurt",
            "1/2 cup mixed berries",
            "1 tbsp chia seeds",
            "1 tsp honey",
        ],
        "instructions": [
            "Spoon Greek yogurt into a serving bowl.",
            "Top with berries and chia seeds.",
            "Drizzle with honey and serve immediately.",
        ],
        "cooking_tips": "Prep dry toppings in jars to assemble this meal in 2 minutes.",
        "tags": "high_protein,kid_friendly",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Spinach Cheese Omelette",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Fluffy omelette packed with greens and melty cheese.",
        "image_url": "https://images.unsplash.com/photo-1510693206972-df098062cb71",
        "ingredients": [
            "3 large eggs",
            "1/2 cup spinach, chopped",
            "30g cheddar cheese, grated",
            "1 tsp olive oil",
        ],
        "instructions": [
            "Whisk eggs with a pinch of salt.",
            "Heat olive oil in a non-stick pan and saute spinach for 1 minute.",
            "Pour in eggs and cook until mostly set.",
            "Add cheese on one side, fold, and cook 30 seconds more.",
        ],
        "cooking_tips": "Use medium-low heat for a tender omelette texture.",
        "tags": "low_carb,high_protein,kid_friendly",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Overnight Oats",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "No-cook breakfast with balanced carbs and healthy fats.",
        "image_url": "https://images.unsplash.com/photo-1517673400267-0251440c45dc",
        "ingredients": [
            "1/2 cup rolled oats",
            "3/4 cup milk",
            "1 tbsp peanut butter",
            "1/2 banana, sliced",
        ],
        "instructions": [
            "Add oats, milk, and peanut butter to a jar.",
            "Stir well until peanut butter is mostly dissolved.",
            "Top with sliced banana, cover, and refrigerate overnight.",
            "Stir and eat cold the next morning.",
        ],
        "cooking_tips": (
            "Add a splash of milk before serving if you prefer a thinner texture."
        ),
        "tags": "high_protein,kid_friendly",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": True,
    },
    {
        "name": "Chicken Salad Wrap",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Light and filling wrap ideal for quick lunches.",
        "image_url": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783",
        "ingredients": [
            "150g cooked chicken breast, diced",
            "2 tbsp plain Greek yogurt",
            "1 whole-wheat wrap",
            "1 cup lettuce",
        ],
        "instructions": [
            "Combine chicken, yogurt, and lemon juice in a bowl.",
            "Lay wrap flat and add lettuce down the center.",
            "Spoon chicken mixture over lettuce and roll tightly.",
            "Slice in half and serve.",
        ],
        "cooking_tips": (
            "Warm the wrap for 10 seconds to prevent tearing while rolling."
        ),
        "tags": "high_protein,kid_friendly",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": True,
    },
    {
        "name": "Tuna Avocado Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Low-carb bowl with healthy fats and plenty of protein.",
        "image_url": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f",
        "ingredients": [
            "1 can tuna in water, drained",
            "1/2 avocado, diced",
            "1 cup cucumber, chopped",
            "1 tbsp olive oil",
        ],
        "instructions": [
            "Add tuna, avocado, and cucumber to a bowl.",
            "Drizzle with olive oil and lemon juice.",
            "Toss gently and season to taste before serving.",
        ],
        "cooking_tips": "Add avocado last and fold gently to keep the pieces intact.",
        "tags": "low_carb,high_protein,carnivore",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Turkey Lettuce Cups",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Crunchy lettuce cups with savory turkey filling.",
        "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd",
        "ingredients": [
            "200g ground turkey",
            "1 tsp soy sauce",
            "1 tsp sesame oil",
            "6 lettuce leaves",
        ],
        "instructions": [
            "Heat a pan over medium heat and cook turkey until browned.",
            "Add garlic, soy sauce, and sesame oil and cook for 1 minute.",
            "Spoon hot filling into lettuce leaves and serve.",
        ],
        "cooking_tips": "Use iceberg or romaine leaves for the best crunch.",
        "tags": "low_carb,high_protein,kid_friendly",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Beef Stir-Fry Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Fast stir-fry with colorful vegetables and tender beef.",
        "image_url": "https://images.unsplash.com/photo-1604908554167-6d8fcb8b7a5e",
        "ingredients": [
            "180g beef strips",
            "1 cup broccoli florets",
            "1/2 bell pepper, sliced",
            "1 tbsp soy sauce",
        ],
        "instructions": [
            "Heat a wok or skillet and cook beef strips for 2 to 3 minutes.",
            "Add broccoli and bell pepper and stir-fry until crisp-tender.",
            "Stir in soy sauce and ginger and cook for 1 minute more.",
            "Serve immediately.",
        ],
        "cooking_tips": "Cook on high heat and avoid overcrowding the pan.",
        "tags": "high_protein,kid_friendly",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Baked Salmon & Asparagus",
        "meal_type": "dinner",
        "difficulty": "full",
        "description": "Simple tray-bake dinner with omega-3 rich salmon.",
        "image_url": "https://images.unsplash.com/photo-1467003909585-2f8a72700288",
        "ingredients": [
            "1 salmon fillet (180g)",
            "1 cup asparagus",
            "1 tbsp olive oil",
            "salt and pepper",
            "1 lemon wedge",
        ],
        "instructions": [
            "Preheat oven to 200C and line a tray with baking paper.",
            "Place salmon and asparagus on tray and drizzle with olive oil.",
            "Season with salt and pepper and bake for 12 to 15 minutes.",
            "Finish with a squeeze of lemon before serving.",
        ],
        "cooking_tips": "Thicker fillets may need 2 to 3 extra minutes in the oven.",
        "tags": "low_carb,high_protein,carnivore",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Beef Meatballs with Zucchini",
        "meal_type": "dinner",
        "difficulty": "full",
        "description": "Juicy meatballs paired with sauteed zucchini ribbons.",
        "image_url": "https://images.unsplash.com/photo-1529563021893-cc83c992d75d",
        "ingredients": [
            "200g ground beef",
            "1 egg",
            "1 small zucchini, sliced",
            "salt",
            "1 tsp olive oil",
        ],
        "instructions": [
            "Preheat oven to 200C and line a tray.",
            "Mix beef, egg, and salt; form into small meatballs.",
            "Bake meatballs for 12 to 15 minutes until cooked through.",
            "Saute zucchini in olive oil for 3 minutes and serve with meatballs.",
        ],
        "cooking_tips": "Wet your hands when shaping meatballs to prevent sticking.",
        "tags": "low_carb,high_protein,kid_friendly,carnivore",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Lemon Garlic Chicken Thighs",
        "meal_type": "dinner",
        "difficulty": "full",
        "description": "Crispy-skinned chicken thighs with bright lemon flavor.",
        "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791",
        "ingredients": [
            "2 chicken thighs",
            "1 tbsp lemon juice",
            "1 garlic clove, minced",
            "1 tsp olive oil",
            "1/4 tsp paprika",
        ],
        "instructions": [
            "Season thighs with salt and paprika.",
            "Heat olive oil and sear thighs skin-side down until golden.",
            "Flip, add garlic and lemon juice, and reduce heat.",
            "Cover and simmer until fully cooked.",
        ],
        "cooking_tips": (
            "Let chicken rest for 3 minutes before serving to keep it juicy."
        ),
        "tags": "low_carb,high_protein,carnivore",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Shrimp Cauliflower Fried Rice",
        "meal_type": "dinner",
        "difficulty": "full",
        "description": "Lower-carb fried rice alternative with quick-cooking shrimp.",
        "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19",
        "ingredients": [
            "200g shrimp, peeled",
            "2 cups cauliflower rice",
            "1 egg",
            "1 tbsp soy sauce",
            "1 tsp sesame oil",
        ],
        "instructions": [
            "Heat a pan and cook shrimp for 2 minutes per side.",
            "Push shrimp aside and scramble egg in the same pan.",
            "Add cauliflower rice and stir-fry for 3 to 4 minutes.",
            "Mix everything together with soy sauce and sesame oil.",
        ],
        "cooking_tips": "Pat shrimp dry before cooking so they sear instead of steam.",
        "tags": "low_carb,high_protein",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": True,
    },
    {
        "name": "Steak & Roasted Veggies",
        "meal_type": "dinner",
        "difficulty": "full",
        "description": "Classic dinner plate with hearty roasted vegetables.",
        "image_url": "https://images.unsplash.com/photo-1558030006-450675393462",
        "ingredients": [
            "220g sirloin steak",
            "1 cup carrots, chopped",
            "1 cup green beans",
            "1 tbsp olive oil",
            "1/2 tsp garlic powder",
        ],
        "instructions": [
            "Toss vegetables with olive oil and garlic powder and roast at 210C.",
            "Season steak with salt and pepper.",
            "Pan-sear steak 3 to 4 minutes per side for medium.",
            "Rest steak for 5 minutes and serve with veggies.",
        ],
        "cooking_tips": "Always rest steak before slicing to keep the juices inside.",
        "tags": "high_protein,carnivore",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Chicken Veggie Soup",
        "meal_type": "dinner",
        "difficulty": "full",
        "description": "Comforting one-pot soup with lean chicken and vegetables.",
        "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554",
        "ingredients": [
            "200g shredded chicken",
            "1 carrot, diced",
            "1 celery stalk, diced",
            "3 cups chicken broth",
            "1/4 tsp thyme",
        ],
        "instructions": [
            "Add broth, carrot, and celery to a pot and bring to a simmer.",
            "Cook vegetables for 10 minutes until tender.",
            "Add shredded chicken and thyme and simmer for 5 minutes.",
            "Season to taste and serve hot.",
        ],
        "cooking_tips": "This soup reheats well, so make extra for meal prep.",
        "tags": "high_protein,kid_friendly",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
]


def _seed_if_empty(db: Session) -> None:
    meals_count = db.query(Meal).count()
    if meals_count > 0:
        return

    for meal_data in SEED_MEALS:
        meal_payload = dict(meal_data)
        meal_payload["ingredients"] = json.dumps(meal_payload["ingredients"])
        meal_payload["instructions"] = json.dumps(meal_payload["instructions"])
        db.add(Meal(**meal_payload))
    db.commit()


def seed_meals() -> None:
    db = SessionLocal()
    try:
        _seed_if_empty(db)
    finally:
        db.close()

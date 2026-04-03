import json

from sqlalchemy.orm import Session

from meal_planner.database.session import SessionLocal
from meal_planner.models.meal import Meal

SEED_MEALS = [
    # BREAKFASTS (8)
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
        "tags": "carnivore,low_carb,high_protein,kid_friendly,simple",
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
        "tags": "high_protein,kid_friendly,heart_healthy,simple",
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
        "tags": "low_carb,high_protein,kid_friendly,simple",
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
            "Add a splash of milk before serving "
            "if you prefer a thinner texture."
        ),
        "tags": "high_protein,kid_friendly,heart_healthy,low_sodium,simple",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": True,
    },
    {
        "name": "Avocado Toast with Poached Egg",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Heart healthy breakfast with great fats and complex carbs.",
        "image_url": "https://images.unsplash.com/photo-1525351484163-7529414344d8",
        "ingredients": [
            "1 slice whole grain bread",
            "1/2 avocado, mashed",
            "1 large egg",
            "Pinch of red pepper flakes",
        ],
        "instructions": [
            "Toast the whole grain bread.",
            "Poach the egg in gently boiling water for 3-4 minutes.",
            "Spread mashed avocado over the toast.",
            "Top with poached egg and red pepper flakes.",
        ],
        "cooking_tips": (
            "Add a dash of vinegar to the boiling water "
            "to help the egg white coagulate."
        ),
        "tags": "heart_healthy,low_sodium,simple",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": False,
    },
    {
        "name": "Smoked Salmon Roll-Ups",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Quick low carb breakfast with high protein and omega-3s.",
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2",
        "ingredients": [
            "100g smoked salmon",
            "2 tbsp cream cheese",
            "1 tbsp fresh dill, chopped",
            "Cucumber slices",
        ],
        "instructions": [
            "Spread cream cheese over smoked salmon slices.",
            "Sprinkle with fresh dill.",
            "Roll up tightly and serve with cucumber slices.",
        ],
        "cooking_tips": (
            "Keep the salmon well chilled before rolling "
            "for easier handling."
        ),
        "tags": "low_carb,high_protein,heart_healthy,simple",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Chia Pudding",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "A heart-healthy, low-sodium breakfast option rich in omega-3.",
        "image_url": "https://images.unsplash.com/photo-1559564109-ce8041d40c06",
        "ingredients": [
            "3 tbsp chia seeds",
            "1 cup almond milk",
            "1/2 tsp vanilla extract",
            "Fresh berries for topping",
        ],
        "instructions": [
            "Mix chia seeds, almond milk, and vanilla in a jar.",
            "Stir well, wait 5 minutes, and stir again to prevent clumping.",
            "Refrigerate overnight or for at least 2 hours.",
            "Top with fresh berries and serve.",
        ],
        "cooking_tips": "Use unsweetened almond milk for lower carb content.",
        "tags": "low_carb,low_sodium,heart_healthy,simple",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": True,
    },
    {
        "name": "Scrambled Tofu",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "A vegan-friendly low-sodium, low-carb breakfast.",
        "image_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec",
        "ingredients": [
            "200g firm tofu, crumbled",
            "1/4 tsp turmeric",
            "1/4 cup spinach",
            "1 tsp olive oil",
        ],
        "instructions": [
            "Heat olive oil in a skillet.",
            "Add crumbled tofu and turmeric, cooking for 3-4 minutes.",
            "Fold in spinach until wilted.",
            "Serve hot.",
        ],
        "cooking_tips": (
            "Press the tofu lightly before crumbling "
            "to remove excess water."
        ),
        "tags": "low_carb,low_sodium,heart_healthy,simple",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },

    # LUNCHES (8)
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
            "Combine chicken, yogurt, and a squeeze of lemon juice in a bowl.",
            "Lay wrap flat and add lettuce down the center.",
            "Spoon chicken mixture over lettuce and roll tightly.",
            "Slice in half and serve.",
        ],
        "cooking_tips": (
            "Warm the wrap for 10 seconds to "
            "prevent tearing while rolling."
        ),
        "tags": "high_protein,kid_friendly,simple",
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
        "tags": "low_carb,high_protein,carnivore,heart_healthy,simple",
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
            "1 tsp low-sodium soy sauce",
            "1 tsp sesame oil",
            "6 lettuce leaves",
        ],
        "instructions": [
            "Heat a pan over medium heat and cook turkey until browned.",
            "Add soy sauce, and sesame oil and cook for 1 minute.",
            "Spoon hot filling into lettuce leaves and serve.",
        ],
        "cooking_tips": "Use iceberg or romaine leaves for the best crunch.",
        "tags": "low_carb,high_protein,kid_friendly,low_sodium,simple",
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
            "Stir in soy sauce and cook for 1 minute more.",
            "Serve immediately.",
        ],
        "cooking_tips": "Cook on high heat and avoid overcrowding the pan.",
        "tags": "high_protein,kid_friendly,low_carb,simple",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Quinoa Salad Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Heart healthy and low sodium quinoa salad.",
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
        "ingredients": [
            "1 cup cooked quinoa",
            "1/2 cup cherry tomatoes, halved",
            "1/4 cup cucumber, diced",
            "1 tbsp lemon juice",
        ],
        "instructions": [
            "Mix quinoa, tomatoes, and cucumber in a bowl.",
            "Drizzle with lemon juice and a tiny splash of olive oil.",
            "Toss well before serving.",
        ],
        "cooking_tips": "Cook quinoa in vegetable broth for extra flavor.",
        "tags": "heart_healthy,low_sodium,simple",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": False,
    },
    {
        "name": "Lentil Soup",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Warm and low-sodium soup.",
        "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554",
        "ingredients": [
            "1 cup cooked lentils",
            "1/4 cup carrots, diced",
            "1/4 cup celery, diced",
            "1 cup low-sodium vegetable broth",
        ],
        "instructions": [
            "Bring broth to a boil in a small pot.",
            "Add lentils, carrots, and celery.",
            "Simmer for 10 minutes until vegetables are tender.",
            "Serve hot.",
        ],
        "cooking_tips": "Add a bay leaf while simmering for extra depth of flavor.",
        "tags": "low_sodium,heart_healthy,high_protein,simple",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Zucchini Noodles with Pesto",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Low carb alternative to pasta.",
        "image_url": "https://images.unsplash.com/photo-1589301773112-0071672e617d",
        "ingredients": [
            "2 cups zucchini noodles",
            "2 tbsp basil pesto",
            "1 tbsp pine nuts",
        ],
        "instructions": [
            "Slightly warm the zucchini noodles in a pan for 1-2 minutes.",
            "Remove from heat and toss with pesto.",
            "Top with pine nuts and serve immediately.",
        ],
        "cooking_tips": "Do not overcook the noodles or they will become mushy.",
        "tags": "low_carb,heart_healthy,simple",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": False,
    },
    {
        "name": "Grilled Chicken Salad",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "High protein and low carb plain salad.",
        "image_url": "https://images.unsplash.com/photo-1505253758473-96b7015fcd40",
        "ingredients": [
            "150g grilled chicken breast",
            "2 cups mixed greens",
            "1 tbsp balsamic vinegar",
            "1 tsp olive oil",
        ],
        "instructions": [
            "Slice grilled chicken breast.",
            "Place over an bed of mixed greens.",
            "Drizzle with balsamic vinegar and olive oil.",
        ],
        "cooking_tips": "Marinade chicken briefly before grilling to keep it moist.",
        "tags": "low_carb,high_protein,low_sodium,simple",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },

    # DINNERS (9)
    {
        "name": "Baked Salmon & Asparagus",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Simple tray-bake dinner with omega-3 rich salmon.",
        "image_url": "https://images.unsplash.com/photo-1467003909585-2f8a72700288",
        "ingredients": [
            "1 salmon fillet (180g)",
            "1 cup asparagus",
            "1 tbsp olive oil",
            "Pinch of black pepper",
            "1 lemon wedge",
        ],
        "instructions": [
            "Preheat oven to 200C and line a tray with baking paper.",
            "Place salmon and asparagus on tray and drizzle with olive oil.",
            "Season with black pepper and bake for 12 to 15 minutes.",
            "Finish with a squeeze of lemon before serving.",
        ],
        "cooking_tips": "Thicker fillets may need 2 to 3 extra minutes in the oven.",
        "tags": "low_carb,high_protein,carnivore,heart_healthy,low_sodium,full_meal",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Beef Meatballs with Zucchini",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Juicy meatballs paired with sauteed zucchini ribbons.",
        "image_url": "https://images.unsplash.com/photo-1529563021893-cc83c992d75d",
        "ingredients": [
            "200g ground beef",
            "1 egg",
            "1 small zucchini, sliced",
            "1 tsp olive oil",
        ],
        "instructions": [
            "Preheat oven to 200C and line a tray.",
            "Mix beef and egg; form into small meatballs.",
            "Bake meatballs for 12 to 15 minutes until cooked through.",
            "Saute zucchini in olive oil for 3 minutes and serve with meatballs.",
        ],
        "cooking_tips": "Wet your hands when shaping meatballs to prevent sticking.",
        "tags": "low_carb,high_protein,kid_friendly,carnivore,full_meal",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Lemon Garlic Chicken Thighs",
        "meal_type": "dinner",
        "difficulty": "full_meal",
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
            "Season thighs with paprika.",
            "Heat olive oil and sear thighs skin-side down until golden.",
            "Flip, add garlic and lemon juice, and reduce heat.",
            "Cover and simmer until fully cooked.",
        ],
        "cooking_tips": (
            "Let chicken rest for 3 minutes before "
            "serving to keep it juicy."
        ),
        "tags": "low_carb,high_protein,carnivore,full_meal",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Shrimp Cauliflower Fried Rice",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Lower-carb fried rice alternative with quick-cooking shrimp.",
        "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19",
        "ingredients": [
            "200g shrimp, peeled",
            "2 cups cauliflower rice",
            "1 egg",
            "1 tbsp low-sodium soy sauce",
            "1 tsp sesame oil",
        ],
        "instructions": [
            "Heat a pan and cook shrimp for 2 minutes per side.",
            "Push shrimp aside and scramble egg in the same pan.",
            "Add cauliflower rice and stir-fry for 3 to 4 minutes.",
            "Mix everything together with soy sauce and sesame oil.",
        ],
        "cooking_tips": "Pat shrimp dry before cooking so they sear instead of steam.",
        "tags": "low_carb,high_protein,low_sodium,full_meal",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": True,
    },
    {
        "name": "Steak & Roasted Veggies",
        "meal_type": "dinner",
        "difficulty": "full_meal",
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
        "tags": "high_protein,carnivore,full_meal",
        "is_carnivore": True,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Chicken Veggie Soup",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Comforting one-pot soup with lean chicken and vegetables.",
        "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554",
        "ingredients": [
            "200g shredded chicken",
            "1 carrot, diced",
            "1 celery stalk, diced",
            "3 cups low-sodium chicken broth",
            "1/4 tsp thyme",
        ],
        "instructions": [
            "Add broth, carrot, and celery to a pot and bring to a simmer.",
            "Cook vegetables for 10 minutes until tender.",
            "Add shredded chicken and thyme and simmer for 5 minutes.",
            "Season to taste and serve hot.",
        ],
        "cooking_tips": "This soup reheats well, so make extra for meal prep.",
        "tags": "high_protein,kid_friendly,low_sodium,heart_healthy,full_meal",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Vegetarian Lentil Shepherd's Pie",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Heart healthy dinner filled with fiber and nutrients.",
        "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554",
        "ingredients": [
            "1 cup cooked lentils",
            "1/2 cup peas and carrots",
            "1 cup mashed sweet potato",
            "1 tsp olive oil",
        ],
        "instructions": [
            "Preheat oven to 200C.",
            "Mix lentils and veggies together with olive oil in a baking dish.",
            "Top evenly with mashed sweet potato.",
            "Bake for 15-20 minutes until hot and bubbly.",
        ],
        "cooking_tips": (
            "Use sweet potatoes for a lower glycemic index "
            "and extra vitamins."
        ),
        "tags": "heart_healthy,low_sodium,full_meal",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": True,
    },
    {
        "name": "Baked Cod with Quinoa",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Low sodium and high protein delicate fish dinner.",
        "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19",
        "ingredients": [
            "1 cod fillet (150g)",
            "1/2 cup cooked quinoa",
            "1/2 cup steamed broccoli",
            "1 wedge lemon",
        ],
        "instructions": [
            "Bake cod at 180C for 12-15 minutes.",
            "Serve baked cod over quinoa alongside steamed broccoli.",
            "Squeeze fresh lemon over the top.",
        ],
        "cooking_tips": "Fish is done when it flakes easily with a fork.",
        "tags": "low_sodium,high_protein,heart_healthy,full_meal",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Mushroom Black Bean Burger",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Heart healthy vegetarian burger alternative.",
        "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349",
        "ingredients": [
            "1 black bean and mushroom patty",
            "1 whole wheat bun",
            "1 slice tomato",
            "1 piece of lettuce",
        ],
        "instructions": [
            "Grill or pan-fry the patty until cooked through.",
            "Assemble the burger with the whole wheat bun, tomato, and lettuce.",
            "Serve hot.",
        ],
        "cooking_tips": "Toast the bun lightly to prevent it from getting soggy.",
        "tags": "heart_healthy,full_meal",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    }
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

import json
from typing import cast

from sqlalchemy.orm import Session

from meal_planner.database.base import Base
from meal_planner.database.session import SessionLocal
from meal_planner.models.meal import Meal

SEED_MEALS = [
    # BREAKFASTS (5)
    {
        "name": "Greek Yogurt Berry & Chia Bowl",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Heart-healthy, low-sodium breakfast bowl rich in protein and fiber.",
        "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "core_base": [
            {
                "name": "1 cup Plain Low-Fat Greek Yogurt",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/2 cup Fresh Mixed Berries",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Chia Seeds",
                "category": "Pantry/Grains",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Chopped Walnuts",
                "category": "Pantry/Grains",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "2 tbsp Honey Granola",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1/2 tsp Ceylon Cinnamon & Extra Chia",
                "category": "Pantry/Grains",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Spoon Greek yogurt into a bowl.",
            "Top with fresh berries, chia seeds, and chopped walnuts.",
            "Family addition: sprinkle honey granola over family portion.",
            "User alternative: sprinkle cinnamon over user portion.",
        ],
        "cooking_tips": "Use unsweetened Greek yogurt to maintain low glycemic impact.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Mediterranean Spinach & Avocado Scramble",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Fluffy egg scramble with fresh spinach and avocado healthy fats.",
        "image_url": "https://images.unsplash.com/photo-1510693206972-df098062cb71",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "core_base": [
            {
                "name": "3 Large Eggs",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1 cup Fresh Baby Spinach",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/2 Avocado (diced)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Extra Virgin Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "2 slices Whole Grain Sourdough Toast",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1/2 cup Sauteed Zucchini Slices",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Whisk eggs gently with cracked black pepper and oregano.",
            "Heat extra virgin olive oil in a skillet and wilt spinach for 1 minute.",
            "Pour in eggs and scramble over medium-low heat until soft curds form.",
            "Fold in diced avocado.",
            "Serve family portion with toasted whole grain bread, and user portion with extra zucchini.",
        ],
        "cooking_tips": "Keep heat low to preserve smooth egg texture and healthy olive oil properties.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Smoked Salmon & Dill Cucumber Plate",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Omega-3 rich wild smoked salmon with crisp cucumber and fresh dill.",
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "core_base": [
            {
                "name": "120g Wild Smoked Salmon",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1 cup Sliced Cucumber",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Fresh Dill (chopped)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Extra Virgin Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 Whole Grain Bagel",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {"name": "1/2 Sliced Avocado", "category": "Produce", "tags": ["user_safe"]}
        ],
        "instructions": [
            "Arrange smoked salmon slices on plates with cucumber rounds.",
            "Drizzle olive oil and sprinkle fresh dill and lemon juice.",
            "Toast bagel for family addition; slice avocado for user side.",
        ],
        "cooking_tips": "Wild salmon provides optimal omega-3 fatty acid profile for cholesterol management.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Tofu & Mushroom Garden Scramble",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Plant-based low-glycemic scramble with turmeric and sautéed mushrooms.",
        "image_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "core_base": [
            {
                "name": "200g Firm Tofu (crumbled)",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 cup Sliced Mushrooms",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/2 cup Bell Peppers (diced)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Extra Virgin Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/4 tsp Turmeric & Black Pepper",
                "category": "Pantry/Grains",
                "tags": ["user_safe", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 Whole Wheat English Muffin",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1 cup Steamed Baby Kale",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Heat olive oil in a skillet and sauté mushrooms and peppers for 3 minutes.",
            "Add crumbled tofu, turmeric, and black pepper; cook for 4-5 minutes until warm.",
            "Serve family with toasted English muffin and user with steamed baby kale.",
        ],
        "cooking_tips": "Turmeric and black pepper work synergistically to reduce systemic inflammation.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Overnight Chia & Almond Butter Pudding",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "No-cook chia pudding packed with soluble fiber and healthy monounsaturated fats.",
        "image_url": "https://images.unsplash.com/photo-1559564109-ce8041d40c06",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,simple",
        "core_base": [
            {
                "name": "3 tbsp Chia Seeds",
                "category": "Pantry/Grains",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 cup Unsweetened Almond Milk",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Natural Almond Butter",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/4 cup Fresh Blueberries",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
        ],
        "family_additions": [
            {"name": "1 Sliced Banana", "category": "Produce", "tags": ["family_side"]}
        ],
        "user_alternatives": [
            {
                "name": "1 tbsp Flaxseed Meal",
                "category": "Pantry/Grains",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Whisk chia seeds, almond milk, and almond butter in jars; chill overnight.",
            "Top with fresh blueberries.",
            "Add sliced banana for family members, and extra flaxseed meal for user.",
        ],
        "cooking_tips": "Soluble chia fiber helps smooth out post-meal glucose response.",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": True,
    },
    # LUNCHES (5)
    {
        "name": "Lemon Herb Chicken & Mediterranean Greens",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Grilled chicken breast over fresh greens, cucumbers, and extra virgin olive oil.",
        "image_url": "https://images.unsplash.com/photo-1505253758473-96b7015fcd40",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "core_base": [
            {
                "name": "180g Grilled Chicken Breast",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "2 cups Mixed Leafy Greens",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/2 Cucumber (sliced)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/4 cup Cherry Tomatoes",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1.5 tbsp Extra Virgin Olive Oil & Lemon",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Cooked Brown Rice",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1 cup Roasted Cauliflower Florets",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Slice grilled chicken breast.",
            "Toss mixed greens, cucumber, and cherry tomatoes with olive oil and fresh lemon juice.",
            "Top salad with sliced chicken.",
            "Serve brown rice for family, and roasted cauliflower for user.",
        ],
        "cooking_tips": "Marinate chicken in lemon juice and oregano for tenderness without added sodium.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Wild Tuna & Avocado Romaine Salad",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Heart-healthy albacore tuna salad tossed with avocado, olive oil, and crunchy celery.",
        "image_url": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "core_base": [
            {
                "name": "1 can Pole-Caught Albacore Tuna (drained)",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1/2 Avocado (mashed)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/2 cup Diced Celery",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Olive Oil Mayonnaise",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Whole Wheat Penne Pasta",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "4 Romaine Lettuce Boat Leaves",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Mix tuna, mashed avocado, diced celery, and olive oil mayo with lemon juice.",
            "For family: toss mixture with cooked whole wheat penne.",
            "For user: spoon tuna avocado mixture into crisp romaine lettuce boats.",
        ],
        "cooking_tips": "Avocado acts as a nutrient-dense substitute for traditional heavy mayonnaise.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Turkey & Broccoli Pepper Stir-Fry",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Lean turkey stir-fry with antioxidant-rich broccoli florets and bell peppers.",
        "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "core_base": [
            {
                "name": "200g Lean Ground Turkey",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 cup Broccoli Florets",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/2 cup Bell Peppers (sliced)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Sesame Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tsp Low-Sodium Tamari",
                "category": "Pantry/Grains",
                "tags": ["user_safe", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Jasmine Brown Rice",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1.5 cups Cauliflower Rice",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Heat sesame oil in a wok and brown turkey thoroughly.",
            "Add broccoli florets and bell peppers; stir-fry for 4 minutes until crisp-tender.",
            "Stir in low-sodium tamari.",
            "Serve family portion over brown rice and user portion over cauliflower rice.",
        ],
        "cooking_tips": "Steaming broccoli lightly preserves its cardiovascular glucosinolates.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Mediterranean Grilled Shrimp & Zucchini Salad",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Succulent grilled wild shrimp with tender zucchini ribbons and olive oil lemon dressing.",
        "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "core_base": [
            {
                "name": "180g Wild Shrimp (peeled)",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1.5 cups Roasted Zucchini Slices",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Extra Virgin Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 Garlic Clove (minced)",
                "category": "Produce",
                "tags": ["user_safe", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Whole Grain Couscous",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1 cup Grilled Asparagus Spears",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Sauté garlic and shrimp in olive oil for 3 minutes until pink.",
            "Toss with roasted zucchini and lemon juice.",
            "Serve family with fluffy couscous and user with additional grilled asparagus.",
        ],
        "cooking_tips": "Shrimp is low in saturated fat and high in heart-healthy minerals.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Heart-Healthy Lentil & Spinach Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "High-fiber brown lentils with sauteed spinach, carrots, and cold-pressed olive oil.",
        "image_url": "https://images.unsplash.com/photo-1547592180-85f173990554",
        "tags": "heart_healthy,low_sodium,user_safe,high_protein,simple",
        "core_base": [
            {
                "name": "1 cup Cooked Brown Lentils",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 cup Baby Spinach",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/2 cup Diced Carrots",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Extra Virgin Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 slice Artisan Whole Grain Bread",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {"name": "1/2 Sliced Avocado", "category": "Produce", "tags": ["user_safe"]}
        ],
        "instructions": [
            "Warm brown lentils with carrots and wilted baby spinach.",
            "Drizzle with cold-pressed olive oil and herbs.",
            "Serve bread for family and sliced avocado for user.",
        ],
        "cooking_tips": "Lentil soluble fiber assists in lowering LDL cholesterol levels.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    # DINNERS (5)
    {
        "name": "Herb Roasted Salmon & Lemon Asparagus",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Premium wild salmon roasted with extra virgin olive oil and tender asparagus spears.",
        "image_url": "https://images.unsplash.com/photo-1467003909585-2f8a72700288",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,full_meal",
        "core_base": [
            {
                "name": "200g Wild Salmon Fillet",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1.5 cups Asparagus Spears",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1.5 tbsp Extra Virgin Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 Lemon Wedge & Herbs",
                "category": "Produce",
                "tags": ["user_safe", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Garlic Butter Brown Rice",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1 cup Cauliflower Rice",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Preheat oven to 200°C (400°F).",
            "Place salmon and asparagus on a parchment-lined baking sheet.",
            "Drizzle generously with extra virgin olive oil, cracked black pepper, and dill.",
            "Bake for 12-14 minutes until salmon flakes easily.",
            "Squeeze fresh lemon before serving.",
            "Serve family portion with Garlic Butter Brown Rice, and user portion with Cauliflower Rice.",
        ],
        "cooking_tips": "Wild salmon provides rich EPA and DHA omega-3s essential for heart health.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Lemon Garlic Baked Cod & Steamed Broccoli",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Flaky white cod baked with fresh garlic, herbs, olive oil, and vibrant steamed broccoli.",
        "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,full_meal",
        "core_base": [
            {
                "name": "200g Fresh Cod Fillet",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "2 cups Broccoli Florets",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Extra Virgin Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 Garlic Clove (minced)",
                "category": "Produce",
                "tags": ["user_safe", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Herb Roasted Yukon Gold Potatoes",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1 cup Sauteed Zucchini Ribbons",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Place cod fillets in baking dish with olive oil, minced garlic, and parsley.",
            "Bake at 190°C (375°F) for 15 minutes.",
            "Steam broccoli florets for 5 minutes.",
            "Serve family with herb roasted Yukon Gold potatoes and user with sautéed zucchini ribbons.",
        ],
        "cooking_tips": "Cod is extremely lean and naturally low in sodium and saturated fats.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Rosemary Chicken Thighs & Roasted Brussels Sprouts",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Juicy skinless chicken thighs pan-roasted with fresh rosemary and crispy Brussels sprouts.",
        "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,full_meal",
        "core_base": [
            {
                "name": "2 Skinless Chicken Thighs",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1.5 cups Brussels Sprouts (halved)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Extra Virgin Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Fresh Rosemary",
                "category": "Produce",
                "tags": ["user_safe", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Wild Rice Blend",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1 cup Steamed Green Beans",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Toss Brussels sprouts in olive oil and roast at 200°C for 20 minutes.",
            "Sear chicken thighs with rosemary in oven-safe skillet until golden and cooked through.",
            "Serve wild rice blend for family and steamed green beans for user.",
        ],
        "cooking_tips": "Brussels sprouts offer potent antioxidants and high dietary fiber.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Grass-Fed Sirloin Steak & Sauteed Green Beans",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Lean sirloin steak seared in olive oil with garlic-infused tender green beans.",
        "image_url": "https://images.unsplash.com/photo-1558030006-450675393462",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,full_meal",
        "core_base": [
            {
                "name": "200g Grass-Fed Sirloin Steak",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1.5 cups Green Beans",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 tbsp Extra Virgin Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/2 tsp Garlic Powder & Black Pepper",
                "category": "Pantry/Grains",
                "tags": ["user_safe", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 large Baked Sweet Potato",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1 cup Sauteed Cremini Mushrooms",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Pan-sear sirloin steak in olive oil over medium-high heat for 3-4 mins per side.",
            "Rest steak 5 minutes before slicing.",
            "Sauté green beans with garlic powder in skillet.",
            "Serve baked sweet potato for family and sautéed mushrooms for user.",
        ],
        "cooking_tips": "Grass-fed beef has a favorable omega-3 to omega-6 ratio compared to conventional beef.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Mediterranean Tofu Steak & Roasted Ratatouille",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Pan-seared firm tofu over colorful roasted eggplant, zucchini, and bell peppers.",
        "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,full_meal",
        "core_base": [
            {
                "name": "200g Firm Tofu (sliced)",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 cup Eggplant (cubed)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1 cup Zucchini (cubed)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1/2 cup Red Bell Pepper",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
            {
                "name": "1.5 tbsp Extra Virgin Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe", "heart_healthy", "low_sodium"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Cooked Quinoa",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "Extra Portion Roasted Ratatouille Veggies",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Roast eggplant, zucchini, and bell pepper with olive oil and Herbs de Provence at 200°C for 20 mins.",
            "Sear tofu slices in olive oil until golden on both sides.",
            "Serve cooked quinoa for family, and extra ratatouille for user.",
        ],
        "cooking_tips": "Soy protein and extra virgin olive oil promote healthy blood lipid balances.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
]


def _seed_if_empty(db: Session) -> None:
    try:
        meals_count = db.query(Meal).count()
        if meals_count > 0:
            first_meal = db.query(Meal).first()
            if first_meal and getattr(first_meal, "core_base", "[]") != "[]":
                return
            db.query(Meal).delete()
            db.commit()
    except Exception:
        db.rollback()
        # Drop and recreate tables if schema missing columns
        bind = db.get_bind()
        Base.metadata.drop_all(bind=bind)
        Base.metadata.create_all(bind=bind)

    for meal_data in SEED_MEALS:
        meal_payload = dict(meal_data)

        core_base_list = cast(list, meal_payload["core_base"])
        family_additions_list = cast(list, meal_payload["family_additions"])
        user_alternatives_list = cast(list, meal_payload["user_alternatives"])

        flat_ingredients = [
            item["name"]
            for item in core_base_list + family_additions_list + user_alternatives_list
        ]

        meal_payload["core_base"] = json.dumps(core_base_list)
        meal_payload["family_additions"] = json.dumps(family_additions_list)
        meal_payload["user_alternatives"] = json.dumps(user_alternatives_list)
        meal_payload["ingredients"] = json.dumps(flat_ingredients)
        meal_payload["instructions"] = json.dumps(meal_payload["instructions"])

        db.add(Meal(**meal_payload))
    db.commit()


def seed_meals() -> None:
    db = SessionLocal()
    try:
        _seed_if_empty(db)
    finally:
        db.close()

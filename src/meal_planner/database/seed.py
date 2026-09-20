import json
from typing import Any, cast

from sqlalchemy.orm import Session

from meal_planner.database.base import Base
from meal_planner.database.session import SessionLocal
from meal_planner.models.meal import Meal

SEED_MEALS: list[dict[str, Any]] = [
    # BREAKFASTS (8)
    {
        "name": "Greek Yogurt Berry & Chia Bowl",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Heart-healthy, low-sodium breakfast bowl rich in protein and fiber.",
        "image_url": "/static/images/greek-yogurt-berry-&-chia-bowl.png",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "calories": 340,
        "protein_g": 24,
        "carbs_g": 32,
        "fats_g": 12,
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
            "Health profile alternative: finish the profile-friendly portion with cinnamon.",
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
        "image_url": "/static/images/mediterranean-spinach-avocado-scramble.jpg",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "calories": 390,
        "protein_g": 21,
        "carbs_g": 8,
        "fats_g": 31,
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
            "Serve the family portion with toasted whole grain bread, and the health-profile portion with extra zucchini.",
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
        "image_url": "/static/images/smoked-salmon-dill-cucumber-plate.jpg",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "calories": 310,
        "protein_g": 26,
        "carbs_g": 6,
        "fats_g": 20,
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
            "Toast the bagel for the family addition; slice avocado for the health-profile side.",
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
        "image_url": "/static/images/tofu-mushroom-garden-scramble.jpg",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "calories": 280,
        "protein_g": 22,
        "carbs_g": 10,
        "fats_g": 18,
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
        "image_url": "/static/images/overnight-chia-almond-butter-pudding.jpg",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,simple",
        "calories": 360,
        "protein_g": 12,
        "carbs_g": 30,
        "fats_g": 22,
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
            "Add sliced banana for family members, and extra flaxseed meal for the health-profile portion.",
        ],
        "cooking_tips": "Soluble chia fiber helps smooth out post-meal glucose response.",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": True,
    },
    {
        "name": "Avocado Toast & Soft Poached Eggs",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Creamy avocado on artisanal whole grain sourdough topped with golden poached eggs.",
        "image_url": "/static/images/avocado-toast-poached-eggs.jpg",
        "tags": "heart_healthy,user_safe,high_protein,simple",
        "calories": 420,
        "protein_g": 18,
        "carbs_g": 35,
        "fats_g": 22,
        "core_base": [
            {
                "name": "2 Large Eggs",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1/2 Avocado (mashed)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1 slice Whole Grain Sourdough",
                "category": "Pantry/Grains",
                "tags": ["user_safe"],
            },
            {
                "name": "1 tsp Extra Virgin Olive Oil & Everything Seasoning",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "2 Crispy Bacon Strips",
                "category": "Protein",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1/2 cup Cherry Tomatoes & Microgreens",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Toast sourdough slice until golden.",
            "Mash avocado with lemon juice and spread generously on toast.",
            "Poach eggs in simmering water for 3 minutes until white is set and yolk is runny.",
            "Top toast with poached eggs, olive oil drizzle, and seasoning.",
        ],
        "cooking_tips": "Add a splash of vinegar to poaching water to keep egg whites tight.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Protein Cinnamon Oat & Berry Bowl",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "Warm rolled oats infused with whey protein, Ceylon cinnamon, and dark berries.",
        "image_url": "/static/images/protein-cinnamon-oat-berry-bowl.jpg",
        "tags": "heart_healthy,high_protein,user_safe,simple",
        "calories": 410,
        "protein_g": 28,
        "carbs_g": 52,
        "fats_g": 8,
        "core_base": [
            {
                "name": "1/2 cup Rolled Oats",
                "category": "Pantry/Grains",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1 scoop Vanilla Protein Powder",
                "category": "Protein",
                "tags": ["user_safe", "high_protein"],
            },
            {
                "name": "1/2 cup Fresh Blackberries & Raspberries",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1 tsp Ceylon Cinnamon",
                "category": "Pantry/Grains",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "1 tbsp Pure Maple Syrup",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1 tbsp Pumpkin Seeds",
                "category": "Pantry/Grains",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Cook rolled oats in water or unsweetened almond milk for 5 minutes.",
            "Remove from heat and stir in protein powder and cinnamon until smooth.",
            "Top with dark berries.",
        ],
        "cooking_tips": "Stir in protein powder after removing oats from direct heat to prevent clumping.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Fluffy Garden Veggie & Goat Cheese Omelet",
        "meal_type": "breakfast",
        "difficulty": "simple",
        "description": "3-egg omelet loaded with cherry tomatoes, spinach, bell peppers, and creamy goat cheese.",
        "image_url": "/static/images/fluffy-garden-veggie-goat-cheese-omelet.jpg",
        "tags": "low_carb,heart_healthy,user_safe,high_protein,simple",
        "calories": 380,
        "protein_g": 26,
        "carbs_g": 8,
        "fats_g": 28,
        "core_base": [
            {"name": "3 Large Eggs", "category": "Protein", "tags": ["user_safe"]},
            {
                "name": "1/2 cup Cherry Tomatoes & Spinach",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "30g Soft Goat Cheese",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
            {
                "name": "1 tbsp Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "1 slice Roasted Breakfast Potatoes",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {"name": "1/2 Sliced Avocado", "category": "Produce", "tags": ["user_safe"]}
        ],
        "instructions": [
            "Whisk eggs with herbs and pour into warm oiled skillet.",
            "Sauté veggies lightly and add to half of omelet along with crumbled goat cheese.",
            "Fold over and serve warm.",
        ],
        "cooking_tips": "Goat cheese adds tangy richness with less lactose than conventional cow cheeses.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    # LUNCHES (8)
    {
        "name": "Lemon Herb Chicken & Mediterranean Greens",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Grilled chicken breast over fresh greens, cucumbers, and extra virgin olive oil.",
        "image_url": "/static/images/lemon-herb-chicken-mediterranean-greens.jpg",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "calories": 440,
        "protein_g": 42,
        "carbs_g": 12,
        "fats_g": 24,
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
            "Serve brown rice for the family, and roasted cauliflower for the health-profile portion.",
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
        "image_url": "/static/images/wild-tuna-avocado-romaine-salad.jpg",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "calories": 380,
        "protein_g": 36,
        "carbs_g": 10,
        "fats_g": 22,
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
            "For the health profile: spoon the tuna avocado mixture into crisp romaine lettuce boats.",
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
        "image_url": "/static/images/turkey-broccoli-pepper-stir-fry.jpg",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "calories": 420,
        "protein_g": 40,
        "carbs_g": 16,
        "fats_g": 22,
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
            "Serve the family portion over brown rice and the health-profile portion over cauliflower rice.",
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
        "image_url": None,
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,simple",
        "calories": 360,
        "protein_g": 34,
        "carbs_g": 12,
        "fats_g": 19,
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
        "image_url": "/static/images/heart-healthy-lentil-spinach-bowl.jpg",
        "tags": "heart_healthy,low_sodium,user_safe,high_protein,simple",
        "calories": 390,
        "protein_g": 20,
        "carbs_g": 54,
        "fats_g": 11,
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
            "Serve bread for the family and sliced avocado for the health-profile side.",
        ],
        "cooking_tips": "Lentil soluble fiber assists in lowering LDL cholesterol levels.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Grilled Chicken Shawarma & Herb Tahini Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Spiced grilled chicken over cucumber tomato salad, pickled onions, and garlic herb tahini.",
        "image_url": None,
        "tags": "heart_healthy,user_safe,high_protein,simple",
        "calories": 520,
        "protein_g": 44,
        "carbs_g": 38,
        "fats_g": 20,
        "core_base": [
            {
                "name": "200g Grilled Chicken Thighs (shawarma spice)",
                "category": "Protein",
                "tags": ["user_safe", "high_protein"],
            },
            {
                "name": "1 cup Cucumber & Tomato Salad",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "2 tbsp Herb Garlic Tahini",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "1 Warm Whole Wheat Pita",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1/2 cup Roasted Cauliflower florets",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Marinate chicken in cumin, coriander, paprika, garlic, and lemon juice; grill thoroughly.",
            "Assemble bowl with salad, sliced chicken, and drizzled tahini dressing.",
        ],
        "cooking_tips": "Tahini provides healthy fats and minerals without dairy.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Pan-Seared Salmon & Quinoa Grain Bowl",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Crispy pan-seared salmon over fluffy quinoa, steamed edamame, and sesame oil dressing.",
        "image_url": None,
        "tags": "heart_healthy,user_safe,high_protein,simple",
        "calories": 560,
        "protein_g": 42,
        "carbs_g": 40,
        "fats_g": 24,
        "core_base": [
            {
                "name": "180g Atlantic Salmon Fillet",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1 cup Cooked White Quinoa",
                "category": "Pantry/Grains",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1/2 cup Shelled Edamame",
                "category": "Produce",
                "tags": ["user_safe", "high_protein"],
            },
            {
                "name": "1 tbsp Toasted Sesame Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "1/4 cup Teriyaki Glaze",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1 tbsp Toasted Sesame Seeds & Lime",
                "category": "Pantry/Grains",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Sear salmon skin-side down in sesame oil for 4 mins, flip and cook 3 mins.",
            "Serve over warm quinoa and shelled edamame.",
        ],
        "cooking_tips": "Quinoa is a complete plant protein containing all 9 essential amino acids.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Chickpea & Roasted Mediterranean Veggie Salad",
        "meal_type": "lunch",
        "difficulty": "simple",
        "description": "Fiber-packed chickpea bowl with roasted red peppers, artichoke hearts, and lemon vinaigrette.",
        "image_url": "/static/images/chickpea-roasted-mediterranean-veggie-salad.jpg",
        "tags": "heart_healthy,low_sodium,user_safe,simple",
        "calories": 430,
        "protein_g": 16,
        "carbs_g": 58,
        "fats_g": 16,
        "core_base": [
            {
                "name": "1.5 cups Cooked Chickpeas",
                "category": "Protein",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1/2 cup Roasted Red Peppers",
                "category": "Produce",
                "tags": ["user_safe"],
            },
            {
                "name": "1/2 cup Artichoke Hearts",
                "category": "Produce",
                "tags": ["user_safe"],
            },
            {
                "name": "1.5 tbsp Olive Oil Lemon Dressing",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "50g Crumbled Feta Cheese",
                "category": "Dairy/Fats",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1/4 cup Kalamata Olives",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Combine chickpeas, roasted peppers, and chopped artichoke hearts.",
            "Toss with olive oil and lemon vinaigrette.",
        ],
        "cooking_tips": "Rinse canned chickpeas under cold water to reduce sodium.",
        "is_carnivore": False,
        "is_high_protein": False,
        "is_kid_friendly": False,
    },
    # DINNERS (8)
    {
        "name": "Herb Roasted Salmon & Lemon Asparagus",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Premium wild salmon roasted with extra virgin olive oil and tender asparagus spears.",
        "image_url": "/static/images/herb-roasted-salmon-lemon-asparagus.jpg",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,full_meal",
        "calories": 510,
        "protein_g": 44,
        "carbs_g": 10,
        "fats_g": 32,
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
            "Serve the family portion with Garlic Butter Brown Rice, and the health-profile portion with Cauliflower Rice.",
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
        "image_url": "/static/images/lemon-garlic-baked-cod-steamed-broccoli.jpg",
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,full_meal",
        "calories": 380,
        "protein_g": 42,
        "carbs_g": 12,
        "fats_g": 18,
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
        "image_url": None,
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,full_meal",
        "calories": 520,
        "protein_g": 46,
        "carbs_g": 14,
        "fats_g": 30,
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
            "Serve wild rice blend for the family and steamed green beans for the health-profile portion.",
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
        "image_url": None,
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,full_meal",
        "calories": 540,
        "protein_g": 50,
        "carbs_g": 10,
        "fats_g": 32,
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
            "Serve baked sweet potato for the family and sautéed mushrooms for the health-profile portion.",
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
        "image_url": None,
        "tags": "low_carb,heart_healthy,low_sodium,user_safe,high_protein,full_meal",
        "calories": 390,
        "protein_g": 26,
        "carbs_g": 22,
        "fats_g": 22,
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
            "Serve cooked quinoa for the family, and extra ratatouille for the health-profile portion.",
        ],
        "cooking_tips": "Soy protein and extra virgin olive oil promote healthy blood lipid balances.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Asian Beef & Broccoli Skillet",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Tender sirloin strips sautéed with broccoli, ginger, garlic, and coconut aminos.",
        "image_url": "/static/images/asian-beef-broccoli-skillet.jpg",
        "tags": "low_carb,heart_healthy,high_protein,full_meal",
        "calories": 540,
        "protein_g": 46,
        "carbs_g": 22,
        "fats_g": 28,
        "core_base": [
            {
                "name": "220g Sirloin Beef Strips",
                "category": "Protein",
                "tags": ["user_safe", "high_protein"],
            },
            {
                "name": "2 cups Broccoli Florets",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1 tbsp Ginger & Garlic (minced)",
                "category": "Produce",
                "tags": ["user_safe"],
            },
            {
                "name": "1 tbsp Sesame Oil & Coconut Aminos",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Steamed White Rice",
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
            "Stir-fry beef strips in hot sesame oil until browned, set aside.",
            "Sauté ginger, garlic, and broccoli until crisp-tender.",
            "Return beef to pan with coconut aminos sauce and toss.",
        ],
        "cooking_tips": "Coconut aminos provide rich savory flavor with less sodium than soy sauce.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Herbed Pork Tenderloin & Roasted Apples",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Lean pork tenderloin roasted with fresh thyme, garlic, and caramelized apple slices.",
        "image_url": "/static/images/herbed-pork-tenderloin-roasted-apples.jpg",
        "tags": "heart_healthy,high_protein,full_meal",
        "calories": 510,
        "protein_g": 42,
        "carbs_g": 32,
        "fats_g": 22,
        "core_base": [
            {
                "name": "200g Lean Pork Tenderloin",
                "category": "Protein",
                "tags": ["user_safe", "high_protein"],
            },
            {
                "name": "1 Green Apple (sliced)",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1 tbsp Fresh Thyme & Garlic",
                "category": "Produce",
                "tags": ["user_safe"],
            },
            {
                "name": "1 tbsp Olive Oil",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Roasted Sweet Potato Wedges",
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
            "Sear pork tenderloin on all sides in an oven-safe skillet.",
            "Arrange apple slices around pork and roast at 200°C for 18 minutes.",
        ],
        "cooking_tips": "Pork tenderloin is as lean as skinless chicken breast.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Baked Turkey Cutlets & Green Beans",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Golden baked turkey cutlets with herbs de Provence and garlic butter green beans.",
        "image_url": "/static/images/baked-turkey-cutlets-green-beans.jpg",
        "tags": "low_carb,heart_healthy,high_protein,full_meal",
        "calories": 480,
        "protein_g": 48,
        "carbs_g": 18,
        "fats_g": 22,
        "core_base": [
            {
                "name": "220g Turkey Breast Cutlets",
                "category": "Protein",
                "tags": ["user_safe", "high_protein"],
            },
            {
                "name": "1.5 cups Fresh Green Beans",
                "category": "Produce",
                "tags": ["user_safe", "heart_healthy"],
            },
            {
                "name": "1 tbsp Olive Oil & Lemon Zest",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "1 cup Garlic Mashed Potatoes",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "1 cup Roasted Yellow Squash",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Season turkey cutlets with lemon zest, rosemary, and olive oil.",
            "Bake at 200°C for 14 minutes.",
            "Sauté green beans in skillet with minced garlic.",
        ],
        "cooking_tips": "Turkey cutlets cook quickly and stay tender when baked with olive oil.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Chana Masala",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Hearty chickpea curry simmered with onion, tomato, garlic, and warming Indian spices.",
        "image_url": "/static/images/chana-masala.jpg",
        "tags": "vegetarian,high_protein,comfort_food,curry,user_safe,spicy",
        "calories": 420,
        "protein_g": 20,
        "carbs_g": 36,
        "fats_g": 16,
        "prep_time_mins": 15,
        "cook_time_mins": 25,
        "servings_default": 4,
        "rating": 4.8,
        "ratings_count": 14,
        "is_favorite": True,
        "prep_detail_steps": [
            {
                "step": 1,
                "title": "Bloom the aromatics",
                "detail": "Sauté onion and garlic in ghee until soft and fragrant.",
            },
            {
                "step": 2,
                "title": "Build the masala",
                "detail": "Add tomatoes, cumin, garam masala, turmeric, and a pinch of salt; simmer until glossy.",
            },
            {
                "step": 3,
                "title": "Finish the curry",
                "detail": "Fold in chickpeas and cook until the sauce thickens and clings to the beans.",
            },
            {
                "step": 4,
                "title": "Serve with style",
                "detail": "Plate over basmati rice and finish with cilantro and a squeeze of lemon.",
            },
        ],
        "core_base": [
            {"name": "1 cup Chickpeas", "category": "Protein", "tags": ["user_safe"]},
            {"name": "1 cup Tomato Base", "category": "Produce", "tags": ["user_safe"]},
            {"name": "1/2 cup Onion", "category": "Produce", "tags": ["user_safe"]},
            {"name": "1 tbsp Ghee", "category": "Dairy/Fats", "tags": ["user_safe"]},
            {
                "name": "1 tsp Garam Masala",
                "category": "Pantry/Grains",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "Basmati Rice",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {"name": "Cauliflower Rice", "category": "Produce", "tags": ["user_safe"]}
        ],
        "instructions": [
            "Sauté onion and garlic in ghee until fragrant.",
            "Add tomatoes, cumin, garam masala, and turmeric; simmer until glossy.",
            "Fold in chickpeas and cook until thickened.",
            "Serve with basmati rice or cauliflower rice.",
        ],
        "cooking_tips": "A squeeze of lemon at the end brightens the curry and balances the richness.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
    {
        "name": "Paneer Butter Masala",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Soft paneer cubes in a silky tomato and cashew butter curry with warming spices.",
        "image_url": "/static/images/paneer-butter-masala.jpg",
        "tags": "vegetarian,comfort_food,curry,user_safe,high_protein",
        "calories": 470,
        "protein_g": 24,
        "carbs_g": 28,
        "fats_g": 29,
        "prep_time_mins": 20,
        "cook_time_mins": 30,
        "servings_default": 3,
        "rating": 4.9,
        "ratings_count": 18,
        "is_favorite": True,
        "prep_detail_steps": [
            {
                "step": 1,
                "title": "Create the base",
                "detail": "Bloom ginger, garlic, and Kashmiri chili in butter until fragrant.",
            },
            {
                "step": 2,
                "title": "Slow the sauce",
                "detail": "Add tomato sauce and allow it to reduce into a glossy, rich curry.",
            },
            {
                "step": 3,
                "title": "Add the paneer",
                "detail": "Stir in cashew cream and gently fold in paneer so it stays tender.",
            },
            {
                "step": 4,
                "title": "Finish the plate",
                "detail": "Serve with naan and a spoon of extra sauce for a restaurant-style finish.",
            },
        ],
        "core_base": [
            {"name": "200g Paneer", "category": "Protein", "tags": ["user_safe"]},
            {
                "name": "1 cup Tomato Sauce",
                "category": "Produce",
                "tags": ["user_safe"],
            },
            {
                "name": "2 tbsp Cashew Cream",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
            {"name": "1 tbsp Butter", "category": "Dairy/Fats", "tags": ["user_safe"]},
            {
                "name": "1 tsp Kashmiri Chili",
                "category": "Pantry/Grains",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {"name": "Naan Bread", "category": "Pantry/Grains", "tags": ["family_side"]}
        ],
        "user_alternatives": [
            {"name": "Steamed Spinach", "category": "Produce", "tags": ["user_safe"]}
        ],
        "instructions": [
            "Bloom ginger, garlic, and chili in butter.",
            "Add tomato sauce and simmer until slightly thickened.",
            "Stir in cashew cream and paneer cubes.",
            "Serve with naan or a side of spinach.",
        ],
        "cooking_tips": "Soak cashews for a smoother sauce and a gentler texture.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": True,
    },
    {
        "name": "Chicken Tikka Masala",
        "meal_type": "dinner",
        "difficulty": "full_meal",
        "description": "Charred chicken in a rich tomato-onion curry finished with cream and cilantro.",
        "image_url": "/static/images/chicken-tikka-masala.jpg",
        "tags": "high_protein,comfort_food,curry,user_safe,spicy",
        "calories": 520,
        "protein_g": 42,
        "carbs_g": 22,
        "fats_g": 28,
        "prep_time_mins": 25,
        "cook_time_mins": 35,
        "servings_default": 4,
        "rating": 4.7,
        "ratings_count": 22,
        "is_favorite": True,
        "prep_detail_steps": [
            {
                "step": 1,
                "title": "Marinate the chicken",
                "detail": "Coat chicken in yogurt, garlic, ginger, and tikka spices for a deep, layered flavor.",
            },
            {
                "step": 2,
                "title": "Char the protein",
                "detail": "Sear until lightly charred for smoky edges and juicy centers.",
            },
            {
                "step": 3,
                "title": "Build the sauce",
                "detail": "Simmer tomato sauce with onions, curry powder, and butter until deeply savory and glossy.",
            },
            {
                "step": 4,
                "title": "Plate elegantly",
                "detail": "Return the chicken to the sauce, finish with cream, and serve with garlic naan.",
            },
        ],
        "core_base": [
            {
                "name": "200g Chicken Breast",
                "category": "Protein",
                "tags": ["user_safe"],
            },
            {
                "name": "1 cup Tomato Curry Sauce",
                "category": "Produce",
                "tags": ["user_safe"],
            },
            {
                "name": "1/4 cup Greek Yogurt",
                "category": "Dairy/Fats",
                "tags": ["user_safe"],
            },
            {"name": "1 tbsp Butter", "category": "Dairy/Fats", "tags": ["user_safe"]},
            {
                "name": "1 tsp Curry Powder",
                "category": "Pantry/Grains",
                "tags": ["user_safe"],
            },
        ],
        "family_additions": [
            {
                "name": "Garlic Naan",
                "category": "Pantry/Grains",
                "tags": ["family_side"],
            }
        ],
        "user_alternatives": [
            {
                "name": "Steamed Cauliflower",
                "category": "Produce",
                "tags": ["user_safe"],
            }
        ],
        "instructions": [
            "Marinate chicken with yogurt and spices, then sear until lightly charred.",
            "Simmer tomato sauce with onion, garlic, and curry powder until reduced.",
            "Return chicken to the sauce and finish with a touch of cream.",
            "Serve with garlic naan or steamed cauliflower.",
        ],
        "cooking_tips": "Short marination keeps the chicken juicy while still absorbing spices.",
        "is_carnivore": False,
        "is_high_protein": True,
        "is_kid_friendly": False,
    },
]


SEED_MEALS.extend(
    [
        {
            "name": "Thai Basil Chicken & Green Beans",
            "meal_type": "dinner",
            "difficulty": "full_meal",
            "description": "Fragrant Thai basil chicken with crisp green beans, chili, garlic, and a light tamari glaze.",
            "image_url": "/static/images/thai-basil-chicken-green-beans.jpg",
            "tags": "thai,high_protein,low_carb,heart_healthy,user_safe,spicy",
            "calories": 430,
            "protein_g": 42,
            "carbs_g": 18,
            "fats_g": 20,
            "core_base": [
                {
                    "name": "200g Chicken Breast",
                    "category": "Protein",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 cup Green Beans",
                    "category": "Produce",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1/2 cup Thai Basil & Bell Pepper",
                    "category": "Produce",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 tbsp Low-Sodium Tamari",
                    "category": "Pantry/Grains",
                    "tags": ["user_safe"],
                },
            ],
            "family_additions": [
                {
                    "name": "1 cup Jasmine Rice",
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
                "Sear chicken with garlic and chili until lightly caramelized.",
                "Add green beans and bell pepper; toss until crisp-tender.",
                "Fold through Thai basil and tamari, then finish with lime.",
                "Serve with jasmine rice or cauliflower rice.",
            ],
            "cooking_tips": "Add the basil off the heat so its aroma stays bright and fresh.",
            "is_carnivore": False,
            "is_high_protein": True,
            "is_kid_friendly": False,
        },
        {
            "name": "Thai Green Curry Tofu & Vegetables",
            "meal_type": "dinner",
            "difficulty": "full_meal",
            "description": "Silky green curry with seared tofu, zucchini, spinach, and aromatic Thai herbs.",
            "image_url": "/static/images/thai-green-curry-tofu-vegetables.jpg",
            "tags": "thai,vegetarian,low_carb,heart_healthy,user_safe,spicy",
            "calories": 390,
            "protein_g": 22,
            "carbs_g": 20,
            "fats_g": 25,
            "core_base": [
                {
                    "name": "200g Firm Tofu",
                    "category": "Protein",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 cup Zucchini & Spinach",
                    "category": "Produce",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1/2 cup Light Coconut Curry Sauce",
                    "category": "Dairy/Fats",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 tbsp Thai Green Curry Paste",
                    "category": "Pantry/Grains",
                    "tags": ["user_safe"],
                },
            ],
            "family_additions": [
                {
                    "name": "1 cup Steamed Jasmine Rice",
                    "category": "Pantry/Grains",
                    "tags": ["family_side"],
                }
            ],
            "user_alternatives": [
                {
                    "name": "Extra Steamed Greens",
                    "category": "Produce",
                    "tags": ["user_safe"],
                }
            ],
            "instructions": [
                "Sear tofu until golden on two sides and set aside.",
                "Bloom green curry paste, then loosen with light coconut sauce.",
                "Simmer zucchini and spinach until just tender; return tofu to the pan.",
                "Finish with lime and cilantro; serve with rice or extra greens.",
            ],
            "cooking_tips": "Keep the curry at a gentle simmer so the coconut sauce stays smooth.",
            "is_carnivore": False,
            "is_high_protein": True,
            "is_kid_friendly": False,
        },
        {
            "name": "Chinese Ginger Scallion Salmon",
            "meal_type": "dinner",
            "difficulty": "full_meal",
            "description": "Silky roasted salmon finished with ginger, scallions, sesame, and a bright low-sodium glaze.",
            "image_url": "/static/images/chinese-ginger-scallion-salmon.jpg",
            "tags": "chinese,high_protein,heart_healthy,low_sodium,user_safe",
            "calories": 470,
            "protein_g": 40,
            "carbs_g": 12,
            "fats_g": 29,
            "core_base": [
                {
                    "name": "200g Salmon Fillet",
                    "category": "Protein",
                    "tags": ["user_safe", "heart_healthy"],
                },
                {
                    "name": "1 tbsp Fresh Ginger & Scallions",
                    "category": "Produce",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 tsp Toasted Sesame Oil",
                    "category": "Dairy/Fats",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 tbsp Low-Sodium Tamari",
                    "category": "Pantry/Grains",
                    "tags": ["user_safe"],
                },
            ],
            "family_additions": [
                {
                    "name": "1 cup Brown Rice",
                    "category": "Pantry/Grains",
                    "tags": ["family_side"],
                }
            ],
            "user_alternatives": [
                {
                    "name": "1 cup Steamed Bok Choy",
                    "category": "Produce",
                    "tags": ["user_safe"],
                }
            ],
            "instructions": [
                "Roast salmon until just cooked and still glossy in the center.",
                "Warm ginger, scallions, sesame oil, and tamari in a small pan.",
                "Spoon the aromatic glaze over the salmon and rest briefly.",
                "Serve with brown rice or steamed bok choy.",
            ],
            "cooking_tips": "Pull the salmon from the oven just before it is fully opaque; carryover heat finishes it gently.",
            "is_carnivore": False,
            "is_high_protein": True,
            "is_kid_friendly": True,
        },
        {
            "name": "Chinese Beef & Broccoli with Garlic",
            "meal_type": "lunch",
            "difficulty": "simple",
            "description": "Tender beef and vivid broccoli tossed in a glossy garlic, ginger, and tamari sauce.",
            "image_url": "/static/images/asian-beef-broccoli-skillet.jpg",
            "tags": "chinese,high_protein,low_carb,user_safe,quick_meal",
            "calories": 450,
            "protein_g": 38,
            "carbs_g": 22,
            "fats_g": 25,
            "core_base": [
                {
                    "name": "180g Lean Beef Strips",
                    "category": "Protein",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1.5 cups Broccoli Florets",
                    "category": "Produce",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 tbsp Garlic & Ginger",
                    "category": "Produce",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 tbsp Low-Sodium Tamari",
                    "category": "Pantry/Grains",
                    "tags": ["user_safe"],
                },
            ],
            "family_additions": [
                {
                    "name": "1 cup Brown Rice",
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
                "Sear beef in a hot wok until browned at the edges; set aside.",
                "Steam-fry broccoli with garlic and ginger until bright green.",
                "Return beef and toss with tamari until the sauce clings.",
                "Serve with brown rice or cauliflower rice.",
            ],
            "cooking_tips": "Cook in batches if needed; a crowded pan steams the beef instead of searing it.",
            "is_carnivore": True,
            "is_high_protein": True,
            "is_kid_friendly": True,
        },
        {
            "name": "German Herb Chicken Schnitzel",
            "meal_type": "dinner",
            "difficulty": "full_meal",
            "description": "Oven-crisp chicken schnitzel with lemon, parsley, and a fresh cucumber herb salad.",
            "image_url": "/static/images/german-herb-chicken-schnitzel.jpg",
            "tags": "german,high_protein,kid_friendly,user_safe,comfort_food",
            "calories": 490,
            "protein_g": 44,
            "carbs_g": 30,
            "fats_g": 22,
            "core_base": [
                {
                    "name": "200g Chicken Breast",
                    "category": "Protein",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1/3 cup Whole-Grain Breadcrumbs",
                    "category": "Pantry/Grains",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 cup Cucumber & Parsley Salad",
                    "category": "Produce",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 tsp Olive Oil & Lemon",
                    "category": "Dairy/Fats",
                    "tags": ["user_safe"],
                },
            ],
            "family_additions": [
                {
                    "name": "1 cup Herb Roasted Potatoes",
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
                "Pound chicken evenly and season with parsley, pepper, and lemon zest.",
                "Coat in whole-grain crumbs and bake until golden and crisp.",
                "Dress cucumber salad with lemon and olive oil.",
                "Serve with roasted potatoes for the family or green beans for the health profile.",
            ],
            "cooking_tips": "Pound the chicken to an even thickness so the crust browns before the center dries out.",
            "is_carnivore": True,
            "is_high_protein": True,
            "is_kid_friendly": True,
        },
        {
            "name": "German Lentil & Roasted Vegetable Bowl",
            "meal_type": "lunch",
            "difficulty": "simple",
            "description": "Earthy lentils with roasted root vegetables, mustard vinaigrette, and fresh herbs.",
            "image_url": "/static/images/heart-healthy-lentil-spinach-bowl.jpg",
            "tags": "german,vegetarian,heart_healthy,high_fiber,user_safe",
            "calories": 380,
            "protein_g": 19,
            "carbs_g": 48,
            "fats_g": 13,
            "core_base": [
                {
                    "name": "1 cup Cooked Brown Lentils",
                    "category": "Protein",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 cup Roasted Carrots & Cabbage",
                    "category": "Produce",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 tbsp Olive Oil & Mustard Vinaigrette",
                    "category": "Dairy/Fats",
                    "tags": ["user_safe"],
                },
                {
                    "name": "1 tbsp Fresh Dill",
                    "category": "Produce",
                    "tags": ["user_safe"],
                },
            ],
            "family_additions": [
                {
                    "name": "1 slice Whole-Grain Rye Bread",
                    "category": "Pantry/Grains",
                    "tags": ["family_side"],
                }
            ],
            "user_alternatives": [
                {
                    "name": "Extra Roasted Cabbage",
                    "category": "Produce",
                    "tags": ["user_safe"],
                }
            ],
            "instructions": [
                "Roast carrots and cabbage until caramelized at the edges.",
                "Warm lentils with dill and a spoon of mustard vinaigrette.",
                "Layer lentils and vegetables in a bowl, then dress while warm.",
                "Serve with rye bread or extra roasted cabbage.",
            ],
            "cooking_tips": "Dress the lentils while warm so they absorb the mustard vinaigrette evenly.",
            "is_carnivore": False,
            "is_high_protein": False,
            "is_kid_friendly": True,
        },
    ]
)


MEAL_TIMING_DEFAULTS = {
    "breakfast": (10, 12),
    "lunch": (15, 20),
    "dinner": (20, 30),
}


def _prep_step_title(index: int, total_steps: int) -> str:
    if index == 1:
        return "Prepare the ingredients"
    if index == total_steps:
        return "Finish and plate"
    if index == 2:
        return "Build the dish"
    return "Bring the flavors together"


def _enrich_seed_meal(meal: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(meal)

    prep_time, cook_time = MEAL_TIMING_DEFAULTS.get(
        enriched.get("meal_type", ""), (15, 20)
    )
    enriched.setdefault("prep_time_mins", prep_time)
    enriched.setdefault("cook_time_mins", cook_time)
    enriched.setdefault("servings_default", 4)
    enriched.setdefault("rating", 4.5)
    enriched.setdefault("ratings_count", 12)
    enriched.setdefault("is_favorite", False)
    enriched.setdefault("nutrition_basis", "per_serving")

    if not enriched.get("prep_detail_steps"):
        instructions = enriched.get("instructions") or []
        enriched["prep_detail_steps"] = [
            {
                "step": index,
                "title": _prep_step_title(index, len(instructions)),
                "detail": instruction,
            }
            for index, instruction in enumerate(instructions, start=1)
        ]

    return enriched


for index, meal in enumerate(SEED_MEALS):
    SEED_MEALS[index] = _enrich_seed_meal(meal)


def _seed_if_empty(db: Session) -> None:
    try:
        meals_count = db.query(Meal).count()
        if meals_count > 0:
            first_meal = db.query(Meal).first()
            if (
                first_meal
                and getattr(first_meal, "calories", 0) > 0
                and meals_count >= len(SEED_MEALS)
            ):
                return
            db.query(Meal).delete()
            db.commit()
    except Exception:
        db.rollback()
        bind = db.get_bind()
        Base.metadata.drop_all(bind=bind)
        Base.metadata.create_all(bind=bind)

    for meal_data in SEED_MEALS:
        meal_payload = _enrich_seed_meal(dict(meal_data))

        core_base_list = cast(list, meal_payload["core_base"])
        family_additions_list = cast(list, meal_payload["family_additions"])
        user_alternatives_list = cast(list, meal_payload["user_alternatives"])
        instructions_list = meal_payload.get("instructions") or []
        prep_detail_steps = meal_payload.get("prep_detail_steps") or []

        flat_ingredients = [
            item["name"]
            for item in core_base_list + family_additions_list + user_alternatives_list
        ]

        meal_payload["core_base"] = json.dumps(core_base_list)
        meal_payload["family_additions"] = json.dumps(family_additions_list)
        meal_payload["user_alternatives"] = json.dumps(user_alternatives_list)
        meal_payload["ingredients"] = json.dumps(flat_ingredients)
        meal_payload["instructions"] = json.dumps(instructions_list)
        meal_payload["prep_detail_steps"] = json.dumps(prep_detail_steps)

        db.add(Meal(**meal_payload))
    db.commit()


def seed_meals() -> None:
    db = SessionLocal()
    try:
        _seed_if_empty(db)
    finally:
        db.close()

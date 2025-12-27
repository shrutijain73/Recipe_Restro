model_response = """"protein = 1
Energy = 2
Carbs = 3
diet_by_region = 4
recipe_with_title = 5

what you want: 1
minp100
maxp500
page1
['180 g butter , melted', '1 cup all-purpose flour', '1 cup sugar', '1 cup of unsweetened desiccated coconut', '1 cup rolled oats', '1 tablespoon golden syrup', '1 teaspoon baking soda', '1/4 teaspoon salt']

Model generated text:
The Anzac Biscuit
Region: Australian
Protein (g): 499.796
Calories: 326.9

Ingredients:
butter
all-purpose flour
sugar
unsweetened desiccated coconut
rolled oats
golden syrup
baking soda
salt

Recipe Instruction:
1. Heat the oven to 350f.
2. Line a baking tray with baking paper.
3. Set aside.
4. In a small saucepan, melt the butter over a medium heat.
5. Add the golden syrup and baking soda to the butter and stir well.
6. Remove from heat and set aside.
7. Mix together the flour, oats, sugar, desiccated coconut and salt in a mixing bowl.
8. Add the melted butter to the dry ingredients and stir with a wooden spoon to combine ingredients.
9. Roll about 1 1/2 tablespoons of dough into small balls and flatten between the palms of your hands.
10. Place dough on baking tray about 4 cm apart to allow room for spreading.
11. Bake the biscuits for about 10-12 minutes or until golden brown.
12. Remove the biscuits from the oven and let them sit on the baking tray for 5 minutes.
13. Remove the biscuits from the tray and cool on a wire rack.
14. Yield, 10-15 biscuits.

Thankyou."""

#includeIngredients = input("includeIngredients").split(" ")
#print(includeIngredients)


includeIngredients = input("Enter ingredients (optional): ") or "None"
if includeIngredients:
    includeIngredients = includeIngredients.split(" ")
print(includeIngredients) 

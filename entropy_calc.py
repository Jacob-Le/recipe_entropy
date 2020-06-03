import csv
import math
import os
import numpy as np

class EntropyCalculator:
    def __init__(self, recipe_dict):
        self.actions = set()
        self.ingredients = set()

        self.actions.add("check_tasty")
        self.actions.add("navigate_tasty")

        self.recipes = {}

        for name, recipe_path in recipe_dict.items():
            with open(recipe_path, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                
                recipe = {
                    "ingredients": [],
                    "actions": []
                }

                for row in reader:
                    if row[1] is not None and row[1] != '':
                        recipe['ingredients'].append(row[1])
                        self.ingredients.add(row[1])
                    if row[2] is not None and row[2] != '':
                        recipe['actions'].append(row[2])
                        self.actions.add(row[2])

                self.recipes[name] = recipe

    def item_prob(self, item, action=False):
        item_set = self.actions if action else self.ingredients
        count = 0
        for name, recipe in self.recipes.items():
            if action and item in recipe['actions']:
                count += 1
            elif not action and item in recipe['ingredients']:
                count += 1
        return count/len(self.recipes)


    def item_entropy(self, item, action=False):
        return -1 * math.log(self.item_prob(item, action=action))

    def recipe_entropy(self, r):
        recipe = self.recipes[r]

        ingr_entropies = {}
        act_entropies = {}

        for ingr in recipe["ingredients"]:
            ingr_entropies[ingr] = self.item_entropy(ingr, action=False)

        for act in recipe["actions"]:
            act_entropies[act] = self.item_entropy(act, action=True)

        sum_ingr = sum(ingr_entropies.values())
        sum_act = sum(act_entropies.values())

        total = sum_ingr + sum_act

        print("recipe: {} | ingredient entropy: {} | action entropy: {} | Total: {}".format(r, sum_ingr, sum_act, total))

        return r, sum_ingr, sum_act, total

if __name__ == "__main__":
    RECIPE_PATH = 'recipes'
    OUTPUT = 'entropy.csv'

    recipes = { r: os.path.join(os.getcwd(), RECIPE_PATH, r) for r in os.listdir(RECIPE_PATH) }

    ec = EntropyCalculator(recipes)

    with open(OUTPUT, 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for recipe in recipes.keys():
            title, sum_ingr, sum_act, total = ec.recipe_entropy(recipe)

            writer.writerow([title, sum_ingr, sum_act, total])

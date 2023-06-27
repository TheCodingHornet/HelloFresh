# -*- coding: utf-8 -*-
#
# File Name:       database.py
# Creation Date:   27/06/2023
# Version:         0.0.1
# Author:          simonstephan Simon STEPHAN <simon.stephan@u-bourgogne.fr>
#
# Copyright (c) 2023,
# All rights reserved. 
#

from py2neo import Relationship, Node, Graph


class Database:
    """
    Description for Database class.
    """

    def __init__(self):
        # Connect to the Neo4j database
        self.graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456789"))

    def count_recipes(self):
        # Count the number of Recipe nodes and return the result
        return self.graph.run("MATCH (r:Recette) RETURN DISTINCT count(r) AS nbRecipes").data()

    def get_recipes(self):
        # Get all distinct Recipe nodes and return them, ordered by name
        return self.graph.run("MATCH (r:Recette) RETURN DISTINCT r AS recette ORDER BY r.name").data()

    def get_cuisines(self):
        # Get all distinct Cuisine nodes and return their names, ordered by name
        cuisines = self.graph.run("MATCH (c:Cuisine) RETURN DISTINCT c.name AS cuisine  ORDER BY c.name").data()
        return [cuisine['cuisine'] for cuisine in cuisines]

    def get_ingredients(self):
        # Get all distinct Ingredient nodes and return their names, ordered by name
        ingredients = self.graph.run("MATCH (i:Ingredient) RETURN DISTINCT i.name AS ingredient ORDER BY i.name").data()
        return [ingredient['ingredient'] for ingredient in ingredients]

    def get_tags(self):
        # Get all distinct Tag nodes and return their names, ordered by name
        tags = self.graph.run("MATCH (t:Tag) RETURN DISTINCT t.name AS tag ORDER BY t.name").data()
        return [tag['tag'] for tag in tags]

    def put_recipes(self, json_datas):
        # Process and store a list of recipes represented as JSON data
        if json_datas is not None:
            for recette_data in json_datas:
                # Create a Recipe node from the recipe data
                recette = Node("Recette",
                               _id=recette_data.get('id'),
                               name=recette_data.get('name'),
                               description=recette_data.get('description'),
                               descriptionHtml=recette_data.get('descriptionHtml'),
                               country=recette_data.get('country'),
                               category=recette_data.get('category.name', ''),
                               difficulty=recette_data.get('difficulty'),
                               headline=recette_data.get('headline'),
                               imageLink=recette_data.get('imageLink'),
                               link=recette_data.get('link'),
                               prepTime=recette_data.get('prepTime'),
                               slug=recette_data.get('slug')
                               )
                # Merge the Recipe node to avoid creating duplicate nodes
                self.graph.merge(recette, "Recette", "_id")

                # Create Allergene nodes and relationships
                for allergene_data in recette_data.get('allergens'):
                    allergene = Node("Allergene",
                                     _id=allergene_data.get('id'),
                                     name=allergene_data.get('name'))
                    self.graph.merge(allergene, "Allergene", "_id")  # Merge to avoid duplicates
                    relation = Relationship(allergene, "ALLERGENE_IN", recette)
                    self.graph.create(relation)

                # Create Cuisine nodes and relationships
                for cuisine_data in recette_data.get('cuisines'):
                    cuisine = Node("Cuisine",
                                   _id=cuisine_data.get('id'),
                                   name=cuisine_data.get('name'))
                    self.graph.merge(cuisine, "Cuisine", "_id")
                    relation = Relationship(cuisine, "CUISINE_OF", recette)
                    self.graph.create(relation)

                # Create Ingredient nodes and relationships
                for ingredient_data in recette_data.get('ingredients'):
                    ingredient = Node("Ingredient",
                                      _id=ingredient_data.get('id'),
                                      name=ingredient_data.get('name'),
                                      quantity=ingredient_data.get('quantity'),
                                      unit=ingredient_data.get('unit'))
                    self.graph.merge(ingredient, "Ingredient", "_id")
                    relation = Relationship(ingredient, "INGREDIENT_IN", recette)
                    self.graph.create(relation)

                # Create Step nodes and relationships
                for step_data in recette_data.get('steps'):
                    id = str(recette_data.get('id')) + "_" + str(step_data.get('index'))
                    step = Node("Step", _id=id, stepNumber=step_data.get('index'),
                                instructions=step_data.get('instructions'),
                                instructionsMarkdown=step_data.get('instructionsMarkdown'),
                                instructionsHTML=step_data.get('instructionsHTML'),
                                utensils=step_data.get('utensils'),
                                images=step_data.get('images.links'),
                                images_str=step_data.get('images.caption'),
                                ingredients=step_data.get('ingredients'))
                    self.graph.merge(step, "Step", "_id")
                    relation = Relationship(step, "STEP_IN", recette)
                    self.graph.create(relation)

                    # Create Tag nodes and relationships
                    for tag_data in recette_data.get('tags'):
                        tag = Node("Tag", _id=tag_data.get('id'), name=tag_data.get('name'))
                        self.graph.merge(tag, "Tag", "_id")
                        relation = Relationship(tag, "TAG_OF", recette)
                        self.graph.create(relation)

    def search(self, selected_cuisine, selected_tag, recipe_name, selected_ingredients):
        # Initialize a list to hold all the conditions
        conditions = []

        # Begin the Cypher query
        q = "MATCH (r:Recette), " \
            "(r:Recette)-[:INGREDIENT_IN]-(i:Ingredient), " \
            "(r:Recette)-[:STEP_IN]-(s:Step), " \
            "(r:Recette)-[:CUISINE_OF]-(c:Cuisine), " \
            "(r:Recette)-[:TAG_OF]-(t:Tag) "

        # Add conditions based on the search parameters
        if selected_cuisine:
            conditions.append(f"c.name = '{selected_cuisine}'")
        if selected_tag:
            conditions.append(f"t.name = '{selected_tag}'")
        if recipe_name:
            conditions.append(f"r.name CONTAINS '{recipe_name}'")
        if selected_ingredients:
            conditions.append(f"i.name IN {selected_ingredients}")

        # Add conditions to the query
        if conditions:
            query = q + " WHERE " + " AND ".join(conditions)
        else:
            query = q

        # Define the return values of the query
        query += " RETURN COLLECT(DISTINCT i) AS Ingredients, " \
                 "COLLECT(DISTINCT s) AS Steps, " \
                 "COLLECT(DISTINCT c) AS Cuisine, " \
                 "COLLECT(DISTINCT t) AS Tags, " \
                 "r AS Recipes, " \
                 "size([(r)-[:INGREDIENT_IN]->(i) | i]) AS NumberOfIngredients, " \
                 "r.prepTime AS PrepTime " \
                 "ORDER BY NumberOfIngredients DESC"

        # Execute the query and return the results
        return self.graph.run(query).data()

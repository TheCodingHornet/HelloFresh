# -*- coding: utf-8 -*-
#
# File Name:       show_window.py
# Creation Date:   27/06/2023
# Version:         0.0.1
# Author:          simonstephan Simon STEPHAN <simon.stephan@u-bourgogne.fr>
#
# Copyright (c) 2023,
# All rights reserved. 
#

from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget


class ShowWindow(QMainWindow):
    """
    This class represents a window to display details of a selected recipe.
    The recipe details include the name, preparation time, ingredients, and steps.
    """

    def __init__(self, data):
        super().__init__()

        recipe = data["Recipes"]

        # Set the window title to the recipe name
        self.setWindowTitle(recipe["name"])

        # Create a QVBoxLayout to add the details of the recipe
        layout = QVBoxLayout()

        # Add labels for each piece of recipe information
        layout.addWidget(QLabel(f"Name: {recipe['name']}"))
        layout.addWidget(QLabel(f"Preparation Time: {recipe['prepTime']}"))
        # layout.addWidget(QLabel(f"Number of Ingredients: {recipe['ingredients']}"))

        # Add a QLabel for each ingredient
        for ingredient in data['Ingredients']:
            layout.addWidget(QLabel(ingredient['name']))

        # Add a QLabel for the steps
        layout.addWidget(QLabel("Steps:"))
        for step in data['Steps']:
            layout.addWidget(QLabel(step['description']))

        # Add the layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

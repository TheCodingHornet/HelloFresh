# -*- coding: utf-8 -*-
#
# File Name:       search_window.py
# Creation Date:   27/06/2023
# Version:         0.0.1
# Author:          simonstephan Simon STEPHAN <simon.stephan@u-bourgogne.fr>
#
# Copyright (c) 2023,
# All rights reserved. 
#

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QListWidget, QLabel, \
    QTableWidget, QTableWidgetItem, QAbstractItemView, QSplitter, QHBoxLayout, QHeaderView
from ui.show_window import ShowWindow


class SearchWindow(QWidget):
    """
    This class represents a search window that allows users to search for recipes based on various parameters.
    The results are displayed in a table.
    """

    def __init__(self, db, parent=None):
        super(SearchWindow, self).__init__(parent)

        self.db = db  # Database object
        self._recipes = None  # A list to store search results

        # Layout and widget setup
        self.layout = QHBoxLayout()
        self.form_layout = QVBoxLayout()

        self.cuisine_label = QLabel("Cuisine:")
        self.cuisine_combo = QComboBox()
        self.cuisine_combo.addItems(db.get_cuisines())
        self.form_layout.addWidget(self.cuisine_label)
        self.form_layout.addWidget(self.cuisine_combo)

        self.ingredient_label = QLabel("Ingredient:")
        self.ingredient_list = QListWidget()
        self.ingredient_list.addItems(db.get_ingredients())
        self.ingredient_list.setSelectionMode(QListWidget.MultiSelection)
        self.form_layout.addWidget(self.ingredient_label)
        self.form_layout.addWidget(self.ingredient_list)

        self.tag_label = QLabel("Tag:")
        self.tag_combo = QComboBox()
        self.tag_combo.addItems(db.get_tags())
        self.form_layout.addWidget(self.tag_label)
        self.form_layout.addWidget(self.tag_combo)

        self.recipe_label = QLabel("Recipe name:")
        self.recipe_line = QLineEdit()
        self.form_layout.addWidget(self.recipe_label)
        self.form_layout.addWidget(self.recipe_line)

        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_recipes)
        self.form_layout.addWidget(self.search_button)

        # Add an empty option to each combo box
        self.cuisine_combo.insertItem(0, "")
        self.tag_combo.insertItem(0, "")

        # By default, set these two fields to 0
        self.cuisine_combo.setCurrentIndex(0)
        self.tag_combo.setCurrentIndex(0)

        # Create the table and set up the columns
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Recipe", "Ingredients", "Cuisine", "Tags"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSortingEnabled(True)

        # Connect the double click signal to the open_show_window method
        self.table.doubleClicked.connect(self.open_show_window)

        # Set up the splitter and layout
        self.splitter = QSplitter(Qt.Horizontal)
        self.form_widget = QWidget()
        self.form_widget.setLayout(self.form_layout)
        self.splitter.addWidget(self.table)
        self.splitter.addWidget(self.form_widget)
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)

        # Set up the table headers
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

    def search_recipes(self):
        """
        This method retrieves the selected parameters and calls the search method of the database with these parameters.
        The search results are then stored in the _recipes list and the table is updated.
        """

        # Get search parameters
        selected_cuisine = self.cuisine_combo.currentText()
        selected_tag = self.tag_combo.currentText()
        recipe_name = self.recipe_line.text()
        selected_ingredients = [item.text() for item in self.ingredient_list.selectedItems()]

        # Call the search method of the database with these parameters
        self._recipes = self.db.search(selected_cuisine, selected_tag, recipe_name, selected_ingredients)

        # Update the table with the search results
        self.update_table()

    def update_table(self):
        """
        This method updates the table with the search results.
        """

        self.table.setRowCount(0)  # Clear the table

        for idx, recipe in enumerate(self._recipes):
            # Insert a new row
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Set the cells of the row
            ingredients = ', '.join([ingredient['name'] for ingredient in recipe['Ingredients']])
            cuisines = ', '.join([cuisine['name'] for cuisine in recipe['Cuisine']])
            tags = ', '.join([tag['name'] for tag in recipe['Tags']])
            self.table.setItem(row, 0, QTableWidgetItem(recipe['Recipes']["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(ingredients))
            self.table.setItem(row, 2, QTableWidgetItem(cuisines))
            self.table.setItem(row, 3, QTableWidgetItem(tags))

    def open_show_window(self, index):
        """
        This method opens a new window to display the selected recipe in detail.
        """

        # Get the selected recipe from the list
        selected_recipe = self._recipes[index.row()]

        # Create and show the ShowWindow
        self.show_window = ShowWindow(selected_recipe)
        self.show_window.show()

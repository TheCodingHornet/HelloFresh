# -*- coding: utf-8 -*-
#
# File Name:       main_window.py
# Creation Date:   27/06/2023
# Version:         0.0.1
# Author:          simonstephan Simon STEPHAN <simon.stephan@u-bourgogne.fr>
#
# Copyright (c) 2023,
# All rights reserved. 
#

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QLabel, QTableWidget, QWidget, QHBoxLayout, \
    QTableWidgetItem, QAbstractItemView, QHeaderView, QMessageBox
from ui.search_window import SearchWindow
from ui.settings_window import SettingsWindow
from utils import Database
from utils.recipe_downloader import RecipeDownloader
import os
import yaml


class MainWindow(QMainWindow):
    """
    This class represents the main window of the application.
    It consists of a table showing the list of recipes and some buttons for different actions like updating the list,
    opening settings, searching, and closing the application.
    """

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Setting up the window
        self.setWindowTitle("Recipe Manager")
        self.setFixedSize(1200, 800)

        # Widget creation
        self.label = QLabel("Label Text")
        self.table = QTableWidget(0, 2)

        # Table configuration
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(["Title", "Uuid"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        # Button creation and signal connection
        self.updateListButton = QPushButton("Update List")
        self.updateListButton.clicked.connect(self.update_list)

        self.settingsButton = QPushButton("Settings")
        self.settingsButton.clicked.connect(self.open_settings)

        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.open_search)

        self.closeAppButton = QPushButton("Close")
        self.closeAppButton.clicked.connect(self.close_app)

        # Layout setup
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.table)

        # Button alignment
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.updateListButton)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.searchButton)
        buttonLayout.addWidget(self.settingsButton)
        buttonLayout.addWidget(self.closeAppButton)
        mainLayout.addLayout(buttonLayout)

        # Central widget setup
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.load_data()

    def load_data(self):
        """
        Loads the recipe data into the table from the database
        """
        self.table.setRowCount(0)  # Clear the table before filling it
        recipes = Database().get_recipes()  # Get the recipes from the database

        for i, recipe in enumerate(recipes):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(recipe['recette']['name']))
            self.table.setItem(i, 1, QTableWidgetItem(recipe['recette']['_id']))

        self.label.setText(f"Number of recipes: {len(recipes)}")

    def update_list(self):
        """
        Update the list of recipes by downloading them and loading them into the table
        """
        if os.path.isfile('settings.yaml'):
            with open('settings.yaml', 'r') as file:
                settings = yaml.safe_load(file)
                downloader = RecipeDownloader(settings)
                db = Database()  # Initialize the database
                downloader.download_recipes(db)  # Pass the database instance to download_recipes

            # Update the table
            self.load_data()
        else:
            QMessageBox.warning(self, "Settings", "Please configure the settings first")

    def open_search(self):
        """
        Open the search window
        """
        db = Database()
        self.window = SearchWindow(db)
        self.window.show()

    def open_settings(self):
        """
        Open the settings window
        """
        settings = SettingsWindow()
        settings.exec_()

    def close_app(self):
        """
        Close the application
        """
        self.close()

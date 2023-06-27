# -*- coding: utf-8 -*-
#
# File Name:       recipe_downloader.py
# Creation Date:   27/06/2023
# Version:         0.0.1
# Author:          simonstephan Simon STEPHAN <simon.stephan@u-bourgogne.fr>
#
# Copyright (c) 2023,
# All rights reserved. 
#

import requests
import time
import os
import json

from PyQt5.QtWidgets import QMessageBox


class RecipeDownloader:
    """
    The RecipeDownloader class is responsible for downloading recipes
    from the HelloFresh API and storing them in a Neo4j database.
    """

    def __init__(self, settings, test=False):
        """
        Initialize RecipeDownloader with provided settings and a flag for test mode.
        """
        self.settings = settings
        self.test = test

    def download_recipes(self, db):
        """
        Download recipes from the HelloFresh API and add them to the Neo4j database.
        """
        # Variable initialization
        if self.test:
            take = 1
            total = 2
        else:
            take = 100
            total = None

        skip = 0

        # Base URL
        url = "https://www.hellofresh.fr/gw/recipes/recipes/search"

        # Loop as long as all recipes have not been fetched
        while total is None or skip < total:

            # Define the path of the cache file
            cache_path = f'datas/{skip // take}.json'

            # Check if the cache file exists and is less than 60 minutes old
            if os.path.exists(cache_path) and time.time() - os.path.getmtime(cache_path) < 60 * 60:
                print(f"Using cached data for page {skip // take}...")
                with open(cache_path, 'r') as file:
                    data = json.load(file)
            else:
                # Build the URL with pagination parameters
                url = f"{url}?take={take}&skip={skip}&country=FR&locale=fr-FR"

                # Set headers with the Bearer Token
                headers = {
                    'Authorization': f"Bearer {self.settings['bearer']}"
                }

                # Make the GET request
                response = requests.get(url, headers=headers)

                # Ensure the request was successful
                if response.status_code != 200:
                    QMessageBox.critical(None, "Error", f"Error {response.status_code}: {response.text}")
                    return

                # Transform the response to JSON
                data = response.json()

                # Save the data to the cache
                with open(cache_path, 'w') as file:
                    json.dump(data, file)

            # Update the total if not already done
            if self.test:
                total = 2
            else:
                if total is None:
                    total = data['total']

            # Add recipes to the database
            db.put_recipes(data['items'])

            print(f"Downloaded {skip} recipes out of {total}...")

            # Update the skip counter for the next request
            skip += take

            # Wait a bit before the next request to not overload the server
            time.sleep(1)

# -*- coding: utf-8 -*-
#
# File Name:       settings_window.py
# Creation Date:   27/06/2023
# Version:         0.0.1
# Author:          simonstephan Simon STEPHAN <simon.stephan@u-bourgogne.fr>
#
# Copyright (c) 2023,
# All rights reserved. 
#

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
import os
import yaml


class SettingsWindow(QDialog):
    """
    This class represents a settings window in which users can enter and save bearer token.
    The bearer token is stored in a file named 'settings.yaml'.
    """

    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 200)

        # Layout setup
        self.layout = QVBoxLayout()

        # Bearer token field setup
        self.bearer_label = QLabel('Bearer:')
        self.bearer_input = QLineEdit()
        self.layout.addWidget(self.bearer_label)
        self.layout.addWidget(self.bearer_input)

        # Save button setup
        self.save_button = QPushButton('Save Settings')
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

        # Connect the save button to the save_settings method
        self.save_button.clicked.connect(self.save_settings)

        # Load existing settings if available
        if os.path.isfile('settings.yaml'):
            with open('settings.yaml', 'r') as file:
                settings = yaml.safe_load(file)
                if settings is not None:
                    # If bearer token is available in the settings, load it into the input field
                    self.bearer_input.setText(settings.get('bearer', ''))

    def save_settings(self):
        """
        This method retrieves the bearer token entered by the user and saves it in the 'settings.yaml' file.
        After saving the settings, it closes the settings window.
        """
        settings = {
            'bearer': self.bearer_input.text()
        }
        with open('settings.yaml', 'w') as file:
            yaml.dump(settings, file)

        self.close()  # Close the settings window

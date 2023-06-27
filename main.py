# -*- coding: utf-8 -*-
#
# File Name:       main.py
# Creation Date:   27/06/2023
# Version:         0.0.1
# Author:          simonstephan Simon STEPHAN <simon.stephan@u-bourgogne.fr>
#
# Copyright (c) 2023,
# All rights reserved. 
#

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

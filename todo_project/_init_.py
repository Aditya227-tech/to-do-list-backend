# Django project initialization
# This file ensures that Python treats this directory as a package
# It can be used to perform any project-wide initialization if needed

import os
import sys

# Optional: Add any project-wide configuration or path settings
# For example, ensuring the project directory is in the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_path)
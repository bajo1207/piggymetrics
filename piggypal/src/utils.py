import os

def get_project_root():
    """
    Returns project src folder
    """
    return os.path.dirname(os.path.abspath(__file__))
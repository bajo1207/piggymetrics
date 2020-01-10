import os

@PendingDeprecationWarning
def get_project_root():
    """
    Returns project src folder
    """
    return os.path.dirname(os.path.abspath(__file__))




SRC_DIR = os.path.dirname(os.path.abspath(__file__))



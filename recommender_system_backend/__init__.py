import os
from dotenv import load_dotenv

project_folder = os.path.expanduser('./')
load_dotenv(os.path.join(project_folder, '.env'))

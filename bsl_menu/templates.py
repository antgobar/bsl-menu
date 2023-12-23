import os

from fastapi.templating import Jinja2Templates


current_directory = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_directory, "templates"))

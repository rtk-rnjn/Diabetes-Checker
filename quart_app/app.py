from quart import Quart

from ml import ML

app = Quart(__name__)
ml = ML(r"quart_app/assests/datasets.csv")
setattr(app, "ml", ml)

from .routes import *  # noqa

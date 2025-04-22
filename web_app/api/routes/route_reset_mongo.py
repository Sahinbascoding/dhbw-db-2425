from flask import redirect, url_for
from src.tools.reset_db import reset_mongo

def reset_mongo_db():
    reset_mongo()
    return redirect(url_for("index"))

from flask import redirect, url_for
from src.tools.reset_db import reset_mysql

def reset_mysql_db():
    reset_mysql()
    return redirect(url_for("index"))

from flask import Blueprint, current_app
import os
from chapinchat.data.db import init_db


reset_bp = Blueprint("reset", __name__)


@reset_bp.delete("/reset")
def reset_api():
    try:
        os.remove(current_app.config["DATABASE"])
    except:
        pass

    init_db(current_app)

    return "All data deleted", 200

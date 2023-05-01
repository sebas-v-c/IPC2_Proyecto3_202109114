from flask import Blueprint, request


reset_bp = Blueprint("reset", __name__)


@reset_bp.delete("/reset")
def reset_api():
    # TODO delete all files
    return "Deleted all files"

import os
from flask import Blueprint, current_app, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from chapinchat.api.users.users_model import save_user_profile


users = Blueprint("users", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@users.post("users/profiles")
def define_profiles():
    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part")
        return "No file"
    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename
    if file.filename == "":
        flash("No selected file")
        return "Empty file"
    if file and allowed_file(file.filename):
        xml_str = file.stream.read()
        # xml_str = str(file.stream.read())
        report = save_user_profile(xml_str)
        return report, 200, {"Content-Type": "application/xml"}

    return "invalid file name"


@users.get("users/weights/<username>")
def user_weights(username):
    return ""


@users.get("users/weights/:all:")
def all_user_weights():
    return ""

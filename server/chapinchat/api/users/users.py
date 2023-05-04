import os
from flask import Blueprint, current_app, flash, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename
import json

import chapinchat.api.messages.messages_model as msg_md
import chapinchat.api.users.users_model as usr_md
import chapinchat.util.graphviz as graph

# from chapinchat.api.users.users_model import save_user_profile


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
        report = usr_md.save_user_profile(xml_str)
        return report, 200, {"Content-Type": "application/xml"}

    return "invalid file name"


@users.get("users/weights/<username>")
def user_weights(username):
    messages = msg_md.get_message_detail(username)

    user_weight = usr_md.get_user_weigth(messages)
    if user_weight is None:
        return ""

    table = usr_md.get_html_table(user_weight)
    file = graph.to_one_table(table)
    return send_file(file, as_attachment=False)


@users.get("users/weights/all/")
def all_user_weights():
    # get an html table by user
    messages = msg_md.get_all_message_detail()

    usr_weight = usr_md.get_all_user_weight(messages)

    tables: list[str] = []
    for list_item in usr_weight:
        try:
            tables.append(usr_md.get_html_table(list_item))
        except:
            continue

    file = graph.all_to_one_table(tables)

    return send_file(file, as_attachment=False)

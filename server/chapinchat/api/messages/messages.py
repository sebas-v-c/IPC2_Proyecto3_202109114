import os
from flask import Blueprint, current_app, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import json

import chapinchat.api.messages.messages_model as msg_md

messages = Blueprint("messages", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@messages.post("messages/new")
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
        report = msg_md.save_new_messages(xml_str)
        return report, 200, {"Content-Type": "application/xml"}

    return "invalid file name"


@messages.get("messages/detail/<username>")
def message_detail(username):
    # get an html string with a table
    try:
        data = request.get_json()
        data = str(data).replace("'", '"')
        data_dict = json.loads(data)
        messages = msg_md.get_message_detail(username, data_dict["date"])
    except:
        messages = msg_md.get_message_detail(username)

    table = msg_md.get_html_table(messages)
    return table


@messages.get("messages/detail/all/")
def all_message_detail():
    # get an html table by user
    try:
        data = request.get_json()
        data = str(data).replace("'", '"')
        data_dict = json.loads(data)
        messages = msg_md.get_all_message_detail(data_dict["date"])
    except:
        messages = msg_md.get_all_message_detail()

    print(messages)
    tables: list[str] = []
    for list_item in messages:
        try:
            tables.append(msg_md.get_html_table(list_item))
        except:
            continue

    return "\n".join(tables)

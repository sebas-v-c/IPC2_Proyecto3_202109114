from flask import Blueprint, request, current_app
import chapinchat.api.messages.messages_model as msg_md
from chapinchat.api.messages.metrics import MessageStats
import chapinchat.api.users.users_model as usr_md
import re

from chapinchat.data.db import DataBase

test_bp = Blueprint("test", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@test_bp.post("/test/")
def test():
    # check if the post request has the file part
    if "file" not in request.files:
        return "No file"
    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename
    if file.filename == "":
        return "Empty file"
    if file and allowed_file(file.filename):
        xml_str = file.stream.read()
        root = ET.fromstring(xml_str)
        new_root = ET.Element("listaMensajes")
        new_root.append(root)

        # xml_str = str(file.stream.read())
        msg_md.save_new_messages(
            ET.tostring(new_root, encoding="utf-8", xml_declaration=True)
        )
        report = test_model(xml_str)
        return report, 200, {"Content-Type": "application/xml"}

    return "invalid file name"


import xml.etree.ElementTree as ET


def test_model(xml) -> str:
    root = ET.fromstring(xml)

    # getting a cleaned file message list
    message_text = root.text
    message_info = message_text.split("Red social: ChapinChat")[0]
    message_info = re.sub(r"\s+", " ", message_info).strip()
    message_body = message_text.split("Red social: ChapinChat")[1]

    # place time
    place_time_regex = r"Lugar y Fecha: ([\w\s]+), (\d{2}/\d{2}/\d{4}) (\d{2}:\d{2})"
    place_time_match = re.search(place_time_regex, message_info, flags=re.UNICODE)
    # place_time_match = place_time_match.group(0)
    # print(place_time_match)
    date = place_time_match.group(2)
    time = place_time_match.group(3)
    # user regex
    user_regex = r"Usuario: [^\s\t\n]+(?:@[^\s\t\n]+)?"
    user_match = re.search(user_regex, message_info, flags=re.UNICODE)

    user_match = user_match.group(0)
    user_name = user_match.split(":")[1].strip()

    DB_NAME = current_app.config["DATABASE"]
    db = DataBase(DB_NAME)

    profiles = db.get_profile_list()
    profile_objects = db.get_all_profiles()
    discarted = db.get_discarted_words()
    msg_stats = MessageStats(user_name, date, time, message_body, profiles)
    msg_stats.remove_words(discarted)
    msg_stats.process_statistics(profile_objects)

    messages_form_user = msg_md.get_message_detail(user_name)
    weigst_from_user = usr_md.get_user_weigth(messages_form_user)

    response_root = ET.Element("respuesta")
    date_time = ET.Element("fechaHora")
    date_time.text = f"{date} {time}"
    user_tag = ET.Element("usuario")
    user_tag.text = user_name
    profile_tag = ET.Element("perfiles")

    response_root.append(date_time)
    response_root.append(user_tag)
    response_root.append(profile_tag)

    for profile in profiles:
        profile_info = ET.Element("perfil", nombre=profile)
        probability = ET.Element("porcentajeProbabilidad")
        probability.text = str(round(msg_stats.profiles[profile], 2))
        actual_weight = ET.Element("pesoActual")
        actual_weight.text = str(round(weigst_from_user.weight[profile], 2))
        profile_info.append(probability)
        profile_info.append(actual_weight)
        profile_tag.append(profile_info)

    # format the response object
    #
    response_string = ET.tostring(response_root, encoding="utf-8", xml_declaration=True)
    xml_string = response_string.decode("utf-8")
    print(xml_string)
    import xml.dom.minidom

    dom = xml.dom.minidom.parseString(xml_string)
    pretty_xml = dom.toprettyxml(indent="    ")
    return pretty_xml

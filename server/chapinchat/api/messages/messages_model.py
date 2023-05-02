import xml.etree.ElementTree as ET
import xml.dom.minidom
import re

from chapinchat.data.db import DataBase
from flask import current_app


def save_new_messages(data) -> str:
    DB_NAME = current_app.config["DATABASE"]
    root = ET.fromstring(data)
    db = DataBase(DB_NAME)

    # getting a cleaned file message list
    message_list = [str(message.text) for message in root]
    message_info = list(
        map(lambda x: x.split("Red social: ChapinChat")[0], message_list)
    )
    message_info = list(map(lambda x: re.sub(r"\s+", " ", x).strip(), message_list))
    message_body = list(
        map(lambda x: x.split("Red social: ChapinChat")[1], message_list)
    )
    user_list = set()

    for i, message in enumerate(message_body):
        # place time
        place_time_regex = (
            r"Lugar y Fecha: ([\w\s]+), (\d{2}/\d{2}/\d{4}) (\d{2}:\d{2})"
        )
        place_time_match = re.search(
            place_time_regex, message_info[i], flags=re.UNICODE
        )
        # place_time_match = place_time_match.group(0)
        # print(place_time_match)
        place = place_time_match.group(1)
        date = place_time_match.group(2)
        time = place_time_match.group(3)
        # user regex
        user_regex = r"Usuario: [^\s\t\n]+(?:@[^\s\t\n]+)?"
        user_match = re.search(user_regex, message_info[i], flags=re.UNICODE)
        user_match = user_match.group(0)
        user_name = user_match.split(":")[1].strip()
        # save message
        db.save_new_message(place, date, time, user_name, message)
        # save new or old user
        db_users = db.get_users_list()
        user_list.add(user_name)
        if not user_name in db_users:
            db.save_new_user(user_name)

    response_root = ET.Element("respuesta")
    users_res = ET.Element("usuarios")
    users_res.text = f"Se procesaron mensajes para {len(user_list)} usuarios distintos"
    message_res = ET.Element("mensajes")
    message_res.text = f"Se procesaron {len(message_list)} mensajes en total"
    response_root.append(users_res)
    response_root.append(message_res)

    # format the response object
    response_string = ET.tostring(response_root, encoding="utf-8", xml_declaration=True)
    return xml.dom.minidom.parseString(response_string).toprettyxml(indent="    ")

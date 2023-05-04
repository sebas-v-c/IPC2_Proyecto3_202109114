import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
from chapinchat.api.messages.metrics import MessageStats

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


# get an html table of
def get_message_detail(username: str, date="") -> list[MessageStats]:
    DB_NAME = current_app.config["DATABASE"]
    db = DataBase(DB_NAME)

    messages = db.get_messages(username=username, date=date)
    if len(messages) == 0:
        return []

    message_objects: list[MessageStats] = []
    profiles = db.get_profile_list()
    profile_objects = db.get_all_profiles()
    discarted = db.get_discarted_words()
    for message in messages:
        text = str(message[5].text)
        msg_stats = MessageStats(
            str(message[3].text),
            str(message[1].text),
            str(message[2].text),
            text,
            profiles,
        )
        msg_stats.remove_words(discarted)

        msg_stats.process_statistics(profile_objects)
        message_objects.append(msg_stats)

    return message_objects


def get_html_table(message_objects: list[MessageStats]) -> str:
    # convert the information objects into a table
    DB_NAME = current_app.config["DATABASE"]
    db = DataBase(DB_NAME)
    profiles = db.get_profile_list()

    build = '<table border="1">'

    build = "\n".join([build, "<tr>"])
    build = "\n".join([build, f"<td><b>{message_objects[0].username}</b></td>"])
    build = "\n".join([build, "</tr>"])

    build = "\n".join([build, "<tr>"])
    build = "\n".join([build, "<td><b>Mensaje</b></td>"])
    for profile in profiles:
        build = "\n".join([build, f'<td><b>% probabilidad perfil "{profile}"</b></td>'])
    build = "\n".join([build, "</tr>"])

    for i, message in enumerate(message_objects):
        build = "\n".join([build, "<tr>"])
        build = "\n".join([build, f"<td>{message.date} {message.time}</td>"])
        for profile in profiles:
            build = "\n".join(
                [build, f"<td>{str(round(message.profiles[profile], 2))} %</td>"]
            )
        build = "\n".join([build, "</tr>"])

    build = "\n".join([build, "</table>"])

    return build


def get_all_message_detail(date="") -> list[list[MessageStats]]:
    DB_NAME = current_app.config["DATABASE"]
    db = DataBase(DB_NAME)

    user_list = db.get_users_list()
    message_by_user: list[list[MessageStats]] = []

    for user in user_list:
        message_by_user.append(get_message_detail(user, date))

    return message_by_user

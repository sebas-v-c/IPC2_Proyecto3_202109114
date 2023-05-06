from typing import Optional
import xml.etree.ElementTree as ET
import xml.dom.minidom
from chapinchat.api.messages.metrics import MessageStats
from chapinchat.api.users.metrics import UserWeights
from chapinchat.data.db import DataBase
from flask import app, current_app


def save_user_profile(data) -> str:
    DB_NAME = current_app.config["DATABASE"]
    root = ET.fromstring(data)
    db = DataBase(DB_NAME)

    response_root = ET.Element("respuesta")

    # Data for profiles
    new_profiles = 0
    updated_profiles = 0

    for profile in root[0]:
        profile_name = profile[0].text
        if db.get_profile(profile_name) is not None:
            db_profile = db.get_profile(profile_name)
            db_word_list = [word.text for word in db_profile[1]]

            word_list = []
            for w in profile[1]:
                if w.text is None:
                    word_list.append(w.attrib["text"])
                else:
                    word_list.append(w.text)

            diff = list(set(word_list) - set(db_word_list))

            for item in diff:
                updated_profiles += 1
                db.save_new_word_in_profile(profile_name, item)
        else:
            new_profiles += 1
            db.save_new_profile(profile)

    # Data for discarted words
    discarted_words = 0
    discarted_list = [word.text for word in root[1]]
    db_discarted_list = db.get_discarted_words()

    diff = list(set(discarted_list) - set(db_discarted_list))
    for item in diff:
        discarted_words += 1
        db.save_new_discarted_word(item)

    new_prof = ET.Element("perfilesNuevos")
    new_prof.text = f"Se han creado {new_profiles} perfiles nuevos"
    old_prof = ET.Element("perfilesExistentes")
    old_prof.text = f"Se han actualizado {updated_profiles} perfiles existentes"
    discarted = ET.Element("descartadas")
    discarted.text = f"Se han creado {discarted_words} nuevas palabras a descartar"
    response_root.append(new_prof)
    response_root.append(old_prof)
    response_root.append(discarted)

    # format the response object
    response_string = ET.tostring(response_root, encoding="utf-8", xml_declaration=True)
    return xml.dom.minidom.parseString(response_string).toprettyxml(indent="    ")


def get_user_weigth(message_list: list[MessageStats]) -> Optional[UserWeights]:
    try:
        user_object = UserWeights(message_list[0].username, {})
    except:
        return None

    weight_dict = dict.fromkeys(message_list[0].profiles.keys(), 0.0)
    for profile, stat in message_list[0].profiles.items():
        profile_stat = []
        for message in message_list:
            if message.profiles[profile] > 0:
                profile_stat.append(message.profiles[profile])
        if len(profile_stat) > 0:
            weight_dict[profile] = sum(profile_stat) / len(profile_stat)

    user_object.weight = weight_dict
    return user_object


def get_html_table(user_weigth: UserWeights) -> str:
    # convert the information objects into a table
    DB_NAME = current_app.config["DATABASE"]
    db = DataBase(DB_NAME)
    profiles = db.get_profile_list()

    build = '<table border="1">'

    build = "\n".join([build, "<tr>"])
    build = "\n".join([build, f"<td><b>{user_weigth.username}</b></td>"])
    build = "\n".join([build, "</tr>"])

    build = "\n".join([build, "<tr>"])
    for profile in profiles:
        build = "\n".join([build, f"<td><b>Peso de Perfil {profile}</b></td>"])
    build = "\n".join([build, "</tr>"])

    build = "\n".join([build, "<tr>"])
    for key, value in user_weigth.weight.items():
        build = "\n".join([build, f"<td>{str(round(value, 2))}</td>"])
    build = "\n".join([build, "</tr>"])

    build = "\n".join([build, "</table>"])

    return build


def get_all_user_weight(users_weights: list[list[MessageStats]]) -> list[UserWeights]:
    DB_NAME = current_app.config["DATABASE"]
    db = DataBase(DB_NAME)

    user_list = db.get_users_list()
    weigt_by_user: list[UserWeights] = []

    for user_w in users_weights:
        weigt_by_user.append(get_user_weigth(user_w))

    return weigt_by_user


# def get_message_detail(username: str, date="") -> list[MessageStats]:
#     DB_NAME = current_app.config["DATABASE"]
#     db = DataBase(DB_NAME)

#     messages = db.get_messages(username=username, date=date)
#     if len(messages) == 0:
#         return []

#     message_objects: list[MessageStats] = []
#     profiles = db.get_profile_list()
#     profile_objects = db.get_all_profiles()
#     discarted = db.get_discarted_words()
#     for message in messages:
#         text = str(message[5].text)
#         msg_stats = MessageStats(
#             str(message[3].text),
#             str(message[1].text),
#             str(message[2].text),
#             text,
#             profiles,
#         )
#         msg_stats.remove_words(discarted)

#         msg_stats.process_statistics(profile_objects)
#         msg_stats.calculate_weights()
#         message_objects.append(msg_stats)

#     return message_objects

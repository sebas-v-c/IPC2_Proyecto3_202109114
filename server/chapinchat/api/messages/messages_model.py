import xml.etree.ElementTree as ET
import xml.dom.minidom
from chapinchat.data.db import DataBase
from flask import current_app


def save_new_messages(data) -> str:
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
            word_list = [word.text for word in profile[1]]

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

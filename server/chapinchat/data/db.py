from typing import Optional
import xml.etree.ElementTree as ET
import os


class DataBase:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        xmlp = ET.XMLParser(encoding="utf-8")
        self.tree = ET.parse(database_path, parser=xmlp)
        self.root = self.tree.getroot()

    def get_profile(self, target_profile) -> Optional[ET.Element]:
        # maybe the user will send invalid query so we first verify
        if target_profile is None:
            return None

        for profile in self.root[0][0]:
            profile_name = profile[0].text
            if profile_name is None:
                return None
            if profile_name == target_profile:
                return profile
        return None

    def get_all_profiles(self) -> list:
        profile_list = []
        for profile in self.root[0][0]:
            dict_profile = {}
            dict_profile["name"] = profile[0].text
            dict_profile["keywords"] = [item.text for item in profile[1]]
            profile_list.append(dict_profile)

        return profile_list

    def get_profile_list(self) -> list:
        return [profile[0].text for profile in self.root[0][0]]

    def get_users_list(self) -> list:
        return [user.text for user in self.root[2]]

    def get_discarted_words(self) -> list:
        return [word.text for word in self.root[0][1]]

    def get_messages(self, username="", date="") -> ET.Element:
        message_list = ET.Element("listaMensajes")

        if username:
            for message in self.root[1]:
                if date:
                    if message[3].text == username and message[1].text == date:
                        message_list.append(message)
                else:
                    if message[3].text == username:
                        message_list.append(message)
        else:
            message_list = self.root[1]

        # if date:
        #     for message in message_list:
        #         if message[1].text != date:
        #             message_list.remove(message)

        return message_list

    def _save(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.tree.write(
                self.database_path,
                encoding="utf-8",
                xml_declaration=True,
                method="xml",
                short_empty_elements=True,
            )

        return wrapper

    @_save
    def save_new_profile(self, new_profile: ET.Element) -> None:
        self.root[0][0].append(new_profile)

    @_save
    def save_new_word_in_profile(self, profile, word) -> None:
        target_profile = self.get_profile(profile)
        new_word = ET.Element("palabra", text=word)

        target_profile[1].append(new_word)

    @_save
    def save_new_discarted_word(self, word) -> None:
        word_element = ET.Element("palabra")
        word_element.text = word
        self.root[0][1].append(word_element)

    @_save
    def save_new_message(self, place, date, time, user, body) -> None:
        message = ET.Element("mensaje")
        place_elem = ET.SubElement(message, "lugar").text = place
        date_elem = ET.SubElement(message, "fecha").text = date
        time_elem = ET.SubElement(message, "hora").text = time
        user_elem = ET.SubElement(message, "usuario").text = user
        social_elem = ET.SubElement(message, "redSocial").text = "ChapinChat"
        body_elem = ET.SubElement(message, "cuerpo").text = body
        self.root[1].append(message)

    @_save
    def save_new_user(self, username) -> None:
        user = ET.Element("usuario")
        user.text = username
        self.root[2].append(user)


def init_db(app):
    db_name = app.config["DATABASE"]
    if not os.path.isfile(db_name):
        with open(db_name, "w+") as db:
            db.write(
                """<?xml version="1.0" encoding="utf-8"?>
<database>
  <configuracion>
    <perfiles>
    </perfiles>
    <descartadas>
    </descartadas>
  </configuracion>
  <listaMensajes>
  </listaMensajes>
  <usuarios>
  </usuarios>
</database>
            """
            )

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
</database>
            """
            )

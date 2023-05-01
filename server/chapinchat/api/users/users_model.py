#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import xml.dom.minidom
from chapinchat.data.db import DataBase
from flask import current_app


def save_user_profile(data) -> str:
    DB_NAME = current_app.config["DATABASE"]
    root = ET.fromstring(data)
    db = DataBase(DB_NAME)
    for profile in root[0]:
        profile_name = profile[0].text
        if db.get_profile(profile_name) is not None:
            print("Actualizar")
        else:
            db.save_new_profile(profile)

    return ""

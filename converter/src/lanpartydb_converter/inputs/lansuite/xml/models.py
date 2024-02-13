"""
lanpartydb_converter.inputs.lansuite.xml.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LANsuite XML data models

:Copyright: 2024 Jochen Kupperschmidt
:License: MIT
"""

from datetime import datetime
from typing import Optional

from pydantic import HttpUrl
from pydantic_xml import BaseXmlModel, element


class Name(BaseXmlModel, tag='name'):
    text: Optional[str] = None


class System(BaseXmlModel, tag='system'):
    version: str = element()
    name: Name
    link: HttpUrl = element()


class Party(BaseXmlModel, tag='party'):
    partyid: str = element()
    name: str = element()
    max_guest: int = element()
    ort: str = element()
    plz: str = element()
    startdate: datetime = element()
    enddate: datetime = element()


class Partys(BaseXmlModel, tag='partys'):
    partys: list[Party]


class Lansuite(BaseXmlModel, tag='lansuite'):
    system: System
    partys: Partys

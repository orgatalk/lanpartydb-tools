"""
lanpartydb_converter.inputs.lansuite.xml.loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LANsuite XML data loader

An XML document with parties is publicly available at
`https://www.yourparty.example/ext_inc/party_infos/infos.xml`.

:Copyright: 2024 Jochen Kupperschmidt
:License: MIT
"""

from pathlib import Path

from lanpartydb_converter.models import Links, Location, Party, Resource

from .models import Lansuite, Party as LansuiteParty


def load_parties(filename: Path) -> list[Party]:
    xml = filename.read_text()
    lansuite = Lansuite.from_xml(xml)

    website_url = str(lansuite.system.link)

    return [
        _build_party(lansuite_party, website_url)
        for lansuite_party in lansuite.partys.partys
    ]


def _build_party(lansuite_party: LansuiteParty, *, website_url: str) -> Party:
    location = Location(
        country_code='de',
        city=lansuite_party.ort,
        zip_code=lansuite_party.plz,
    )

    links = Links(website=Resource(url=website_url))

    return Party(
        slug=lansuite_party.partyid,
        title=lansuite_party.name,
        start_on=lansuite_party.startdate.date(),
        end_on=lansuite_party.enddate.date(),
        location=location,
        links=links,
    )

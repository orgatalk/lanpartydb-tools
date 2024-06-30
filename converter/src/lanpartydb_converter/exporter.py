"""
lanpartydb_converter.exporter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data exporter

:Copyright: 2024 Jochen Kupperschmidt
:License: MIT
"""

import dataclasses
from datetime import date
from pathlib import Path
from typing import Any

import tomlkit

from .models import Party


def export_parties(parties: list[Party], output_path: Path) -> Path:
    """Export parties to separate TOML files."""
    # Output path should not exist yet. Raise exception if it does.
    output_path.mkdir()

    parties = _select_parties_in_past(parties)

    for party in parties:
        export_party(party, output_path)


def _select_parties_in_past(parties: list[Party]) -> list[Party]:
    """Return only parties that happened in the past."""
    today = date.today()
    return [party for party in parties if party.end_on < today]


def export_party(party: Party, output_path: Path) -> Path:
    """Export party to TOML file."""
    filename = output_path / f'{party.slug}.toml'
    content = serialize_party(party)
    filename.write_text(content)


def serialize_party(party: Party) -> str:
    """Serialize party to TOML document."""
    party_dict = _party_to_sparse_dict(party)
    _handle_links(party_dict)
    return tomlkit.dumps(party_dict)


def _party_to_sparse_dict(party: Party) -> dict[str, Any]:
    data = dataclasses.asdict(party)
    _remove_default_values(data)
    return data


def _remove_default_values(d: dict[str, Any]) -> dict[str, Any]:
    """Remove `None` values from first level of dictionary."""
    for k, v in list(d.items()):
        if (v is None) or (v is False):
            del d[k]
        elif isinstance(v, dict):
            _remove_default_values(v)

    return d


def _handle_links(party_dict: dict[str, Any]):
    links_dict = party_dict.pop('links')
    if links_dict:
        website_dict = links_dict.pop('website', None)
        if website_dict:
            offline = website_dict.get('offline', False)
            if offline:
                website_dict['offline'] = offline
                website = website_dict
            else:
                website = website_dict['url']
            links_dict['website'] = website
            party_dict['links'] = links_dict

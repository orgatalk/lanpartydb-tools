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

    output_data = _party_to_sparse_dict(party)

    with filename.open('w') as f:
        tomlkit.dump(output_data, f)


def _party_to_sparse_dict(party: Party) -> dict[str, Any]:
    data = dataclasses.asdict(party)

    _remove_none_values(data)

    return data


def _remove_none_values(d: dict[str, Any]) -> dict[str, Any]:
    """Remove `None` values from first level of dictionary."""
    for k, v in list(d.items()):
        if v is None:
            del d[k]
        elif isinstance(v, dict):
            _remove_none_values(v)

    return d

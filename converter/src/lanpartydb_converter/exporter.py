"""
lanpartydb_converter.exporter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data exporter

:Copyright: 2024 Jochen Kupperschmidt
:License: MIT
"""

import dataclasses
from pathlib import Path
from typing import Any

import tomlkit

from .models import Party


def export_party(party: Party, output_path: Path) -> Path:
    """Export party to TOML file."""
    # Output path should not exist yet. Raise exception if it does.
    output_path.mkdir()

    filename = output_path / f'{party.slug}.toml'

    output_data = _party_to_sparse_dict(party)

    with filename.open('w') as f:
        tomlkit.dump(output_data, f)


def _party_to_sparse_dict(party: Party) -> dict[str, Any]:
    data = dataclasses.asdict(party)

    # Remove `None` values.
    for k, v in list(data.items()):
        if v is None:
            del data[k]

    return data

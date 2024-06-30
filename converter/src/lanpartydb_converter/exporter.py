"""
lanpartydb_converter.exporter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data exporter

:Copyright: 2024 Jochen Kupperschmidt
:License: MIT
"""

from datetime import date
from pathlib import Path

from lanpartydb.models import Party
from lanpartydb.writing import serialize_party


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

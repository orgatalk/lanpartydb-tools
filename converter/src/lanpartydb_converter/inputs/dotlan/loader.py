"""
lanpartydb_converter.inputs.dotlan.loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DOTLAN Intranet data loader (SQLite-based)

Expects an SQL dump of the DOTLAN database that includes both `CREATE
TABLE` as well as `INSERT INTO` statements for tables `events` and
`event_location`.

To create it from the DOTLAN admin:

* Navigate to "Support Tools".
* Select just those two tables.
* Tick checkboxes "Export structure" and "Export data".
* Select "none" for compression.

:Copyright: 2024 Jochen Kupperschmidt
:License: MIT
"""

from datetime import date, datetime
from pathlib import Path
import sqlite3

from lanpartydb_converter.models import Links, Location, Party, Resource


def load_parties(sql_filename: Path, base_url: str) -> list[Party]:
    sql = sql_filename.read_text()
    sql = _filter_sql(sql)

    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.executescript(sql)

    cursor.execute(
        """
        SELECT e.id, e.name, e.begin, e.end, e.anzahl, l.name AS location_name, l.countrycode, l.city, l.zip, l.street
        FROM events AS e
        LEFT JOIN event_location AS l ON l.id = e.location_id
    """
    )
    rows = cursor.fetchall()

    return [_build_party(row, base_url) for row in rows]


BEGINNINGS_TO_DROP = {'-- ', 'DROP ', 'KEY ', 'SET '}


def _filter_sql(original_sql: str) -> str:
    linebreak = '\n'

    original_lines = original_sql.split(linebreak)

    def _generate_lines():
        for line in original_lines:
            if _exclude_line(line):
                continue

            # Remove comma after last `CREATE TABLE` argument.
            if line.lstrip().startswith('PRIMARY KEY'):
                line = line.rstrip(',')

            if line.lstrip().startswith(') ENGINE='):
                line = ');'

            yield line

    filtered_sql = linebreak.join(_generate_lines())

    filtered_sql = filtered_sql.replace(' AUTO_INCREMENT', '')
    filtered_sql = filtered_sql.replace(
        ' CHARACTER SET latin1 COLLATE latin1_german1_ci', ''
    )

    return filtered_sql


def _exclude_line(line: str) -> bool:
    return any(map(line.lstrip().startswith, BEGINNINGS_TO_DROP))


def _build_party(row, base_url: str) -> Party:
    party_id = str(row['id'])

    return Party(
        slug=f'party-{party_id}',
        title=row['name'],
        start_on=_parse_date(row['begin']),
        end_on=_parse_date(row['end']),
        seats=int(row['anzahl']),
        location=Location(
            name=row['location_name'],
            country_code=row['countrycode'],
            city=row['city'],
            zip_code=row['zip'],
            street=row['street'],
        ),
        links=Links(
            website=Resource(url=f'{base_url}/party/{party_id}'),
        ),
    )


def _parse_date(value: str) -> date:
    return datetime.fromisoformat(value).date()

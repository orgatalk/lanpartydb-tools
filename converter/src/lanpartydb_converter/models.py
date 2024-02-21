"""
lanpartydb_converter.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data models

:Copyright: 2024 Jochen Kupperschmidt
:License: MIT
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Series:
    slug: str
    name: str
    alternative_names: set[str] = field(default_factory=set)


@dataclass(frozen=True, kw_only=True)
class Party:
    slug: str
    title: str
    series_slug: str | None = field(kw_only=True, default=None)
    organizer_entity: str | None = field(kw_only=True, default=None)
    start_on: date
    end_on: date
    seats: int | None = None
    online: bool | None = False
    location: Location | None = None
    links: Links | None = None


@dataclass(frozen=True)
class Location:
    name: str | None = field(kw_only=True, default=None)
    country_code: str
    city: str
    zip_code: str | None
    street: str | None = field(kw_only=True, default=None)


@dataclass(frozen=True)
class Links:
    website: str | None

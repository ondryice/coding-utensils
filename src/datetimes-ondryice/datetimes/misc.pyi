"""Basic module for constants & functions involving date/time objects and operations."""

from datetime import date, datetime, timedelta, timezone, UTC
from typing import Literal, overload

from datetimes.timedelta_tuples import TimeDeltaTuple

UTC
PROGRAM_START: datetime
"""Timezone-aware datetime object (in the system's default timezone), representing the instant this module was imported."""
LOCAL_TIME: timezone
"""The system's default timezone."""

def now (tzinfo = LOCAL_TIME, /) -> datetime:
  """Returns the current date/time."""
def today (tzinfo = LOCAL_TIME, /) -> date:
  """Returns the current date, taking timezone into account."""

@overload
def td_rounded (timedelta: timedelta, spec: Literal['dd','hh','mm','ss','ms','us'], /) -> timedelta:
  """Rounds the provided timedelta to the nearest unit of measure of the provided specificity."""
@overload
def td_rounded (tuple: TimeDeltaTuple, spec: Literal['dd','hh','mm','ss','ms','us'], /) -> TimeDeltaTuple: ...
@overload
def td_rounded (
  timedelta: timedelta,
  spec: Literal['days','hours','minutes','seconds','milliseconds','microseconds',
    'day','hour','minute','second','millisecond','microsecond',
    'day','hr','min','sec','milli','micro'
  ],
/) -> timedelta: ...
@overload
def td_rounded (
  tuple: TimeDeltaTuple,
  spec: Literal['days','hours','minutes','seconds','milliseconds','microseconds',
    'day','hour','minute','second','millisecond','microsecond',
    'day','hr','min','sec','milli','micro'
  ],
/) -> TimeDeltaTuple: ...

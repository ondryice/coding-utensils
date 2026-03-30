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

@overload
def td_string (timedelta: timedelta, spec: Literal['auto','dd','hh','mm','ss','ms','us'] = 'auto', /) -> str:
  """Generates a well-formatted timedelta string, by default rounding the timedelta to make TD strings more readable.

  Will (generally) trim leading zeros from the front, and unless specificity is overridden, will also trail much of the tail, providing by default a maximum of three distinct units of measure.
  For example, if the # of days is non-zero, will return something like "{dd}D {hh}:{mm}", otherwise if # hours is non-zero, will return something like "{hh}:{mm}:{ss}", and so on.
  Exceptionally, when reporting timedeltas under a minute in duration, will format as decimal numbers with appropriate SI unit name suffices.
  For example, for `timedelta(seconds=12, microseconds=45_999)`, the result would be "12.046s".
  Another note, unlike typical timedelta objects, negative durations will read more friendily for humans.
  In the case above, `timedelta(seconds=-12, microseconds=-45_999)`, the result would be "-12.046s".
  Instead of only negating the `days` property, it is simply reported _as if it were positive_ (ie `abs()`), with the difference that the entire string is prefixed with the minus sign.
  """
@overload
def td_string (tuple: TimeDeltaTuple, spec: Literal['auto','dd','hh','mm','ss','ms','us'] = 'auto', /) -> str: ...
@overload
def td_string (
  timedelta: timedelta,
  spec: Literal['days','hours','minutes','seconds','milliseconds','microseconds',
    'day','hour','minute','second','millisecond','microsecond',
    'day','hr','min','sec','milli','micro'
  ],
/) -> str: ...
@overload
def td_string (
  tuple: TimeDeltaTuple,
  spec: Literal['days','hours','minutes','seconds','milliseconds','microseconds',
    'day','hour','minute','second','millisecond','microsecond',
    'day','hr','min','sec','milli','micro'
  ],
/) -> str: ...

@overload
def td_tuple (timedelta: timedelta, spec: Literal['dd','hh','mm','ss','ms','us'] = 'us', /) -> TimeDeltaTuple:
  """Simple factory method for the TimeDeltaTuple class, optionally with rounding the provided delta to the provided specificity."""
@overload
def td_tuple (
  timedelta: timedelta,
  spec: Literal['days','hours','minutes','seconds','milliseconds','microseconds',
    'day','hour','minute','second','millisecond','microsecond',
    'day','hr','min','sec','milli','micro'
  ],
/) -> TimeDeltaTuple: ...

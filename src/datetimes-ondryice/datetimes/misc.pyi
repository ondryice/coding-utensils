from datetime import date, datetime, timezone, UTC

UTC
PROGRAM_START: datetime
"""Timezone-aware datetime object (in the system's default timezone), representing the instant this module was imported."""
LOCAL_TIME: timezone
"""The system's default timezone."""

def now (tzinfo = LOCAL_TIME, /) -> datetime:
  """Returns the current date/time."""
def today (tzinfo = LOCAL_TIME, /) -> date:
  """Returns the current date, taking timezone into account."""

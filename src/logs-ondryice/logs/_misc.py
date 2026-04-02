from datetime import datetime, time, UTC

PROGRAM_START = datetime.now(UTC).astimezone()
LOCAL_TIME = PROGRAM_START.tzinfo

def instant (instant: datetime|time = ...):
  if instant is ...:
    return datetime.now(LOCAL_TIME)
  elif isinstance(instant, datetime):
    if instant.tzinfo:
      return instant
    return instant.astimezone(LOCAL_TIME)
  elif isinstance(instant, time):
    return datetime(
      PROGRAM_START.year, PROGRAM_START.month, PROGRAM_START.day,
      instant.hour, instant.minute, instant.second, instant.microsecond,
      tzinfo=(instant.tzinfo if instant.tzinfo else LOCAL_TIME),
    )
  raise TypeError(f"invalid type for instant {instant!r} - must be datetime or time")

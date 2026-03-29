from datetime import datetime, UTC

PROGRAM_START = datetime.now(UTC).astimezone()
LOCAL_TIME = PROGRAM_START.tzinfo

def now (tz=...):
  if tz is ...:
    tz = LOCAL_TIME
  return datetime.now(tz)
def today (tz=...):
  return now(tz).date()

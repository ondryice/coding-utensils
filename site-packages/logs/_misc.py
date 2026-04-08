from datetime import datetime, time, timedelta

PROGRAM_START = datetime.now().astimezone()
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

def td_string (value, rounding='auto', /):
  if not isinstance(value, timedelta):
    raise TypeError(f"invalid type for value {value!r} - {type(value).__name__} is not supported")
  dd = hh = mm = ss = ms = us = 0
  seconds = 0.
  def split_td ():
    nonlocal dd, hh, mm, ss, ms, us, seconds
    dd, ss, us = value.days, value.seconds, value.microseconds
    ms, us = divmod(us, 1000)
    mm, ss = divmod(ss, 60)
    hh, mm = divmod(mm, 60)
    seconds = value.total_seconds()

  sign, value = '-'*(value.days < 0), abs(value)
  split_td()

  rounding = str(rounding).lower()
  rounding = dict(
    microsecond='us', millisecond='ms', second='ss',
    minute='mm', hour='hh', day='dd',
  ).get(rounding.removesuffix('s'), dict(
    micro='us', milli='ms', sec='ss', min='mm', hr='hh',
  ).get(rounding, rounding))
  if rounding == 'auto':
    if dd: rounding = 'mm'
    elif hh: rounding = 'ss'
    elif mm or ss: rounding = 'ms'
    else: rounding = 'us'

  if rounding != 'us':
    match (rounding):
      case 'ms': value = timedelta(milliseconds=round(seconds * 1_000))
      case 'ss': value = timedelta(seconds=round(seconds))
      case 'mm': value = timedelta(minutes=round(seconds / 60))
      case 'hh': value = timedelta(hours=round(seconds / 3_600))
      case 'dd': value = timedelta(days=round(seconds / 86_400))
    split_td()

  if rounding == 'dd': return f"{sign}{dd:,}D"
  if rounding == 'hh': return f"{sign}{dd:,}D {hh}H"
  if rounding == 'mm': return f"{sign}{dd:,}D {hh:02}:{mm:02}"
  if dd:
    if rounding == 'ss': return f"{sign}{dd:,}D {hh:02}:{mm:02}:{ss:02}"
    if rounding == 'ms': return f"{sign}{dd:,}D {hh:02}:{mm:02}:{ss:02}.{ms:03}"
    if rounding == 'us': return f"{sign}{dd:,}D {hh:02}:{mm:02}:{ss:02}.{ms:03}{us:03}"
  if rounding == 'ss': return f"{sign}{hh:02}:{mm:02}:{ss:02}"
  if hh:
    if rounding == 'ms': return f"{sign}{hh:02}:{mm:02}:{ss:02}.{ms:03}"
    if rounding == 'us': return f"{sign}{hh:02}:{mm:02}:{ss:02}.{ms:03}{us:03}"
  if mm: return f"{sign}{mm:02}:{ss:02}.{ms:03}" + (rounding=='us')*f"{us:03}"
  if ss: return f"{sign}{ss}.{ms:03}" + (rounding=='us')*f"{us:03}" + 's'
  if ms: return f"{sign}{ms}.{us:03}ms"
  return f"{sign}{us}us"

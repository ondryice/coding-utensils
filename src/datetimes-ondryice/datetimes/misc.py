from datetime import datetime, timedelta, UTC

PROGRAM_START = datetime.now(UTC).astimezone()
LOCAL_TIME = PROGRAM_START.tzinfo

def now (tz=...):
  if tz is ...:
    tz = LOCAL_TIME
  return datetime.now(tz)
def today (tz=...):
  return now(tz).date()

def td_rounded (value, spec: str, /):
  from datetimes.timedelta_tuples import TimeDeltaTuple as tdt
  if isinstance(value, timedelta):
    delta = tdt.new(value)
  elif isinstance(value, tdt):
    delta = value
  else:
    raise TypeError(f"invalid type for value {value!r} - {type(value).__name__} is not supported")
  spec = spec.lower()
  spec = dict(
    microsecond='us', millisecond='ms', second='ss',
    minute='mm', hour='hh', day='dd',
  ).get(spec.removesuffix('s'), dict(
    micro='us', milli='ms', sec='ss', min='mm', hr='hh',
  ).get(spec, spec))
  def result (dd=0, hh=0, mm=0, ss=0, ms=0, us=0):
    if isinstance(value, timedelta): return timedelta(dd, ss, us, ms, mm, hh)
    return tdt(dd, hh, mm, ss, ms, us)
  match (spec):
    case 'us': return result(us=delta.asmicroseconds())
    case 'ms': return result(ms=round(delta.asmilliseconds()))
    case 'ss': return result(ss=round(delta.asseconds()))
    case 'mm': return result(mm=round(delta.asminutes()))
    case 'hh': return result(hh=round(delta.ashours()))
    case 'dd': return result(dd=round(delta.asdays()))
  raise ValueError(f"invalid spec {spec!r} - must be 'dd', 'hh', 'mm', 'ss', 'ms', or 'us', or an alias of one of these")

from datetime import datetime, timedelta, UTC

PROGRAM_START = datetime.now(UTC).astimezone()
LOCAL_TIME = PROGRAM_START.tzinfo

def now (tz=...):
  if tz is ...:
    tz = LOCAL_TIME
  return datetime.now(tz)
def today (tz=...):
  return now(tz).date()

def td_rounded (value, spec, /):
  from datetimes.timedelta_tuples import TimeDeltaTuple as tdt
  if isinstance(value, timedelta):
    delta = tdt.new(value)
  elif isinstance(value, tdt):
    delta = value
  else:
    raise TypeError(f"invalid type for value {value!r} - {type(value).__name__} is not supported")
  spec = str(spec).lower()
  spec = dict(
    microsecond='us', millisecond='ms', second='ss',
    minute='mm', hour='hh', day='dd',
  ).get(spec.removesuffix('s'), dict(
    micro='us', milli='ms', sec='ss', min='mm', hr='hh',
  ).get(spec, spec))
  def result (dd=0, hh=0, mm=0, ss=0, ms=0, us=0):
    if isinstance(value, timedelta): return timedelta(dd, ss, us, ms, mm, hh)
    return tdt.new(timedelta(dd, ss, us, ms, mm, hh))
  match (spec):
    case 'us': return result(us=delta.asmicroseconds())
    case 'ms': return result(ms=round(delta.asmilliseconds()))
    case 'ss': return result(ss=round(delta.asseconds()))
    case 'mm': return result(mm=round(delta.asminutes()))
    case 'hh': return result(hh=round(delta.ashours()))
    case 'dd': return result(dd=round(delta.asdays()))
  raise ValueError(f"invalid spec {spec!r} - must be 'dd', 'hh', 'mm', 'ss', 'ms', or 'us', or an alias of one of these")

def td_string (value, spec='auto', /):
  from datetimes.timedelta_tuples import TimeDeltaTuple as tdt
  if isinstance(value, timedelta):
    delta = tdt.new(value)
  elif isinstance(value, tdt):
    delta = value
  else:
    raise TypeError(f"invalid type for value {value!r} - {type(value).__name__} is not supported")
  spec = str(spec).lower()
  spec = dict(
    microsecond='us', millisecond='ms', second='ss',
    minute='mm', hour='hh', day='dd',
  ).get(spec.removesuffix('s'), dict(
    micro='us', milli='ms', sec='ss', min='mm', hr='hh',
  ).get(spec, spec))
  sign, delta = '-'*(delta.dd < 0), abs(delta)
  if spec == 'auto':
    if delta.dd: spec = 'mm'
    elif delta.hh: spec = 'ss'
    elif delta.mm or delta.ss: spec = 'ms'
    else: spec = 'us'
  delta = td_rounded(delta, spec)
  if spec == 'dd': return f"{sign}{delta.dd:,}D"
  if spec == 'hh': return f"{sign}{delta.dd:,}D {delta.hh}H"
  if spec == 'mm': return f"{sign}{delta.dd:,}D {delta.hh:02}:{delta.mm:02}"
  if delta.dd:
    if spec == 'ss': return f"{sign}{delta.dd:,}D {delta.hh:02}:{delta.mm:02}:{delta.ss:02}"
    if spec == 'ms': return f"{sign}{delta.dd:,}D {delta.hh:02}:{delta.mm:02}:{delta.ss:02}.{delta.ms:03}"
    if spec == 'us': return f"{sign}{delta.dd:,}D {delta.hh:02}:{delta.mm:02}:{delta.ss:02}.{delta.ms:03}{delta.us:03}"
  if spec == 'ss': return f"{sign}{delta.hh:02}:{delta.mm:02}:{delta.ss:02}"
  if delta.hh:
    if spec == 'ms': return f"{sign}{delta.hh:02}:{delta.mm:02}:{delta.ss:02}.{delta.ms:03}"
    if spec == 'us': return f"{sign}{delta.hh:02}:{delta.mm:02}:{delta.ss:02}.{delta.ms:03}{delta.us:03}"
  if delta.mm: return f"{sign}{delta.mm:02}:{delta.ss:02}.{delta.ms:03}" + (spec=='us')*f"{delta.us:03}"
  if delta.ss: return f"{sign}{delta.ss}.{delta.ms:03}" + (spec=='us')*f"{delta.us:03}" + 's'
  if delta.ms: return f"{sign}{delta.ms}.{delta.us:03}ms"
  return f"{sign}{delta.us}us"

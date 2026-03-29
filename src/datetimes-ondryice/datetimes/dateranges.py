from datetime import date
from typing import Sequence, final

@final
class daterange (Sequence[date]):
  def __init__(self, *args):
    USAGE = ("usage: "
      f"{type(self).__name__}(start: date|ISO, stop: date|ISO[, step: int]), "
      f"{type(self).__name__}(start: date|ISO, numdays: int[, step: int]), or "
      f"{type(self).__name__}(numdays: int, stop: date|ISO[, step: int])"
    )
    if len(args) not in (2,3):
      raise TypeError(f"invalid number of arguments {len(args)} - expected 2 or 3; {USAGE}")
    a1, a2, step = [ *args, 1 ][:3]
    start = stop = None
    if isinstance(a1, date):
      start = a1.toordinal()
      if isinstance(a2, date):
        stop = a2.toordinal()
      elif isinstance(a2, int):
        stop = start + a2 * step
    elif isinstance(a1, int) and isinstance(a2, date):
      stop = a2.toordinal()
      start = stop - a1 * step
    if start is None or stop is None:
      raise TypeError(f"invalid types provided {args} - {USAGE}")
    self._r = range(start, stop, step)

  @property
  def start (self):
    return date.fromordinal(self._r.start)
  @property
  def stop (self):
    return date.fromordinal(self._r.stop)
  @property
  def step (self):
    return self._r.step

  def __len__ (self):
    return self._r.__len__()
  def __iter__ (self):
    return map(date.fromordinal, self._r)
  def __getitem__ (self, key, /):
    if isinstance(key, slice):
      cp = object.__new__(type(self))
      cp._r = self._r.__getitem__(key)
      return cp
    o = self._r.__getitem__(key)
    assert isinstance(o, int)
    return date.fromordinal(o)

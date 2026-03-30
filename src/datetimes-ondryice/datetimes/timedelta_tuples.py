from datetime import timedelta
from typing import NamedTuple

class TimeDeltaTuple (NamedTuple):
  dd: int = 0
  hh: int = 0
  mm: int = 0
  ss: int = 0
  ms: int = 0
  us: int = 0
  @property
  def days (self):
    return self.dd
  @property
  def hours (self):
    return self.hh
  @property
  def minutes (self):
    return self.mm
  @property
  def seconds (self):
    return self.ss
  @property
  def milliseconds (self):
    return self.ms
  @property
  def microseconds (self):
    return self.us

  def asdays (self):
    return self.astimedelta().total_seconds() / 86_400
  def ashours (self):
    return self.astimedelta().total_seconds() / 3_600
  def asminutes (self):
    return self.astimedelta().total_seconds() / 60
  def asseconds (self):
    return round(self.astimedelta().total_seconds(), 6)
  def asmilliseconds (self):
    return round(self.astimedelta().total_seconds() * 1_000, 3)
  def asmicroseconds (self):
    return round(self.astimedelta().total_seconds() * 1_000_000)
  def astimedelta (self):
    return timedelta(self.dd, self.ss, self.us, self.ms, self.mm, self.hh)

  @classmethod
  def new (cls, obj, /):
    if isinstance(obj, timedelta):
      ms, us = divmod(obj.microseconds, 1_000)
      mm, ss = divmod(obj.seconds, 60)
      hh, mm = divmod(mm, 60)
      dd = obj.days
      return TimeDeltaTuple(dd, hh, mm, ss, ms, us)
    raise TypeError(f"invalid type for value {obj!r} - expected timedelta")

  def __str__ (self):
    from datetimes.misc import td_string
    return td_string(self, 'auto')

  def __eq__ (self, value, /):
    if self is value:
      return True
    if isinstance(value, TimeDeltaTuple):
      return self.astimedelta().__eq__(value.astimedelta())
    if isinstance(value, timedelta):
      return self.astimedelta().__eq__(value)

  def __abs__ (self):
    return type(self).new(abs(self.astimedelta()))

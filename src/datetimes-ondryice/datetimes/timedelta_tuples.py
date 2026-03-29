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
  def astimedelta (self):
    return timedelta(self.dd, self.ss, self.us, self.ms, self.mm, self.hh)

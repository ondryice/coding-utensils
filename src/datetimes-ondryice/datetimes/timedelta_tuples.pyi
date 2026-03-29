"""Module for the `TimeDeltaTuple` class."""

from datetime import timedelta
from typing import Literal, NamedTuple, overload

class TimeDeltaTuple (NamedTuple):
  """Class for representing timedeltas as sums of distinct measures."""
  dd: int = 0
  hh: int = 0
  mm: int = 0
  ss: int = 0
  ms: int = 0
  us: int = 0

  @property
  def days (self) -> int: ...
  @property
  def hours (self) -> int: ...
  @property
  def minutes (self) -> int: ...
  @property
  def seconds (self) -> int: ...
  @property
  def milliseconds (self) -> int: ...
  @property
  def microseconds (self) -> int: ...

  def astimedelta (self) -> timedelta: ...
  @classmethod
  def new (self, timedelta: timedelta, /) -> TimeDeltaTuple: ...
  
  def __abs__ (self) -> TimeDeltaTuple: ...

  @overload
  def __eq__ (self, value: TimeDeltaTuple|timedelta, /) -> bool: ...
  @overload
  def __eq__ (self, value, /) -> Literal[False]: ...

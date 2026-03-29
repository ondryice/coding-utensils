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

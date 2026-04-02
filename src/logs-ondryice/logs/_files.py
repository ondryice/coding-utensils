from datetime import datetime
from io import TextIOWrapper

from logs._misc import instant as _inst, PROGRAM_START

class LOGFILE:
  file: None|TextIOWrapper
  times: list[datetime]
  indent: int
  blocked: int
  def __new__ (cls, file, start=..., /):
    if file is None: pass
    elif isinstance(file, TextIOWrapper) and file.writable(): pass
    else: raise ValueError(f"invalid file {file!r} - must be None for stdout or writable instance of io.TextIOWrapper")
    start = PROGRAM_START if start is ... else _inst(start)
    obj = super().__new__(LOGFILE)
    obj.file = file
    obj.times = [ start ]
    obj.indent = obj.blocked = 0
    return obj
  def block (self):
    self.blocked += 1
    return self
  def unblock (self):
    self.blocked -= self.blocked > 0
    return self

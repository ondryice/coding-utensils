from contextlib import contextmanager
from datetime import datetime
from io import TextIOWrapper

from logs._misc import instant as _inst, td_string, PROGRAM_START

class LOGFILE:
  __logfile_instances: dict[TextIOWrapper,LOGFILE]
  file: None|TextIOWrapper
  times: list[datetime]
  indent: int
  locked: int
  def __new__ (cls, file, start, /):
    if file is None: return STDOUT
    elif isinstance(file, TextIOWrapper) and file.writable():
      if file in LOGFILE.__logfile_instances:
        return LOGFILE.__logfile_instances[file]
    else: raise ValueError(f"invalid file {file!r} - must be None for stdout or writable instance of io.TextIOWrapper")
    start = _inst(start)
    obj = super().__new__(LOGFILE)
    obj.file = file
    obj.times = [ start ]
    obj.indent = obj.locked = 0
    LOGFILE.__logfile_instances[file] = obj
    return obj
  def lock (self):
    self.locked += 1
    return self
  def unlock (self):
    self.locked -= self.locked > 0
    return self
  def enter (self, instant=...):
    if self.locked:
      return self
    self.times.append(_inst(instant))
    self.indent += 1
    return self
  def escape (self):
    if self.locked:
      return self
    if not self.indent:
      raise RuntimeError("cannot escape section - output already at zero-level indent")
    self.times.pop()
    self.indent -= 1
    return self

  def push (self, *values, sep=' ', end='\n', flush=False):
    if self.locked:
      return self
    print(*values, sep=sep, end=end, file=self.file, flush=flush)
    return self
  @contextmanager
  def pushandlockif (self, condition: bool, values, sep=' ', end='\n', flush=False):
    if condition and not self.locked:
      yield self.push(*values, sep=sep, end=end, flush=flush).lock()
      self.unlock()
    else:
      yield self

  def note (self, message, instant: datetime, timestamp=True, runtime=False, flush=False):
    if self.locked:
      return self
    parts = [
      (' '*10,f"[{instant:%H:%M:%S}]")[timestamp],
      '  '*self.indent + '-',
      str(message),
      f"({td_string(instant-self.times[-1])})"
    ][:3+runtime]
    return self.push(*parts, flush=flush)

STDOUT = object.__new__(LOGFILE)
STDOUT.file, STDOUT.times = None, [ PROGRAM_START ]
STDOUT.indent = STDOUT.locked = 0
LOGFILE.__logfile_instances = {}

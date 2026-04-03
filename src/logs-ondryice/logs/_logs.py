from contextlib import contextmanager
from datetime import datetime

from logs._errors import LogSectionExit, LoggingError, NegativeLogIndentError
from logs._files import STDOUT
from logs._misc import instant as _inst

class log:
  output = STDOUT
  forwarding = False
  muted = blocked = 0
  sectionindent = None

  @classmethod
  def super (cls) -> None|type[log]:
    if cls is log:
      return None
    elif issubclass(cls, log):
      return cls.__base__
    raise TypeError(f"cannot get super log for {cls.__name__} - not a subclass of log")

  @classmethod
  def mute (cls):
    cls.muted += 1
    return cls
  @classmethod
  def unmute (cls):
    cls.muted -= cls.muted > 0
    return cls
  @classmethod
  def block (cls):
    cls.blocked += 1
    return cls
  @classmethod
  def unblock (cls):
    cls.blocked -= cls.blocked > 0
    return cls

  @classmethod
  def enter (cls, instant=...):
    instant = _inst(instant)
    with STDOUT.enterandlock(instant):
      with cls.output.enterandlock(instant):
        if cls.super():
          cls.super().enter(instant)
    return cls
  @classmethod
  def escape (cls):
    return cls.__escapemany(1)
  @classmethod
  def __escapemany (cls, num):
    if num < 1:
      return cls
    if cls.output.indent < num:
      raise NegativeLogIndentError(cls)
    with STDOUT.escapeandlock(num):
      with cls.output.escapeandlock(num):
        if cls.super():
          cls.super().__escapemany(num)
    return cls

  @classmethod
  def push (cls, *values, sep=' ', end='\n', flush=False):
    with STDOUT.pushandlockif(not cls.muted, values, sep, end, flush):
      with cls.output.pushandlockif(not cls.blocked, values, sep, end, flush):
        if cls.forwarding and cls.super():
          cls.super().push(*values, sep=sep, end=end, flush=flush)
    return cls
  @classmethod
  def space (cls, lines=1, flush=False):
    if lines < 1:
      return cls
    return cls.push('\n'*lines, end='', flush=flush)
  @classmethod
  def note (cls, message, instant=..., timestamp=True, runtime=False, flush=False):
    args = str(message), _inst(instant), bool(timestamp), bool(runtime), bool(flush)
    def __note (lc: type[log]):
      with STDOUT.noteandlockif(not lc.muted, *args):
        with lc.output.noteandlockif(not lc.blocked, *args):
          if lc.forwarding and lc.super():
            __note(lc.super())
    __note(cls); return cls
  @classmethod
  def start (cls, header, instant=..., timestamp=True, runtime=False, flush=False):
    instant = _inst(instant)
    return cls.note(header, instant, timestamp, runtime, flush).enter(instant)
  @classmethod
  def finish (cls, message='Done.', instant=..., timestamp=True, runtime=True, flush=...):
    instant = _inst(instant)
    if cls.output.indent == cls.sectionindent:
      cls.exit(message, instant, timestamp, runtime, (True if flush is ... else flush))
    elif flush is ...:
      flush = False
    return cls.note(message, instant, timestamp, runtime, flush).escape()

  @contextmanager
  @classmethod
  def section (cls, header, instant=..., timestamp=True, runtime=False, flush=False):
    instant = _inst(instant)
    prev = cls.sectionindent
    cls.start(header, instant, timestamp, runtime, flush)
    cls.sectionindent = cls.output.indent
    try:
      yield
      cls.exit(instant=datetime.now())
    except LogSectionExit as exit:
      cls.__escapemany(cls.output.indent - cls.sectionindent)
      cls.note(*exit.note)
      cls.__escapemany(1)
    except Exception as error:
      instant = datetime.now().astimezone()
      if cls.output.indent > cls.sectionindent:
        cls.note(f"!!! Caught unhandled {type(error).__name__} !!!", runtime=True)
        cls.__escapemany(cls.output.indent - cls.sectionindent)
      cls.note(f"!!! Aborted section - caught unhandled {type(error).__name__}:")
      cls.push(error, flush=True)
    finally: cls.sectionindent = prev
  @classmethod
  def exit (cls, message="Finished section.", instant=..., timestamp=True, runtime=True, flush=True):
    instant = _inst(instant)
    if cls.sectionindent is None:
      raise LoggingError(cls, f"cannot exit {cls.__name__} section - {cls.__name__} is not in a section")
    raise LogSectionExit(cls, str(message), _inst(instant), bool(timestamp), bool(runtime), bool(flush))

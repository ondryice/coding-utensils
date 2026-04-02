from logs._files import STDOUT

class log:
  output = STDOUT
  forwarding = False
  muted = blocked = 0

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
  def push (cls, *values, sep=' ', end='\n', flush=False):
    if not cls.super():
      if not cls.blocked:
        STDOUT.write(*values, sep=sep, end=end, flush=flush)
      return cls
    if (std:=not cls.muted):
      STDOUT.write(*values, sep=sep, end=end, flush=flush).lock()
    if (file:=not cls.blocked):
      cls.output.write(*values, sep=sep, end=end, flush=flush).lock()
    if cls.forwarding:
      cls.super().push(*values, sep=sep, end=end, flush=flush)
    STDOUT.unlock(std)
    cls.output.unlock(file)
    return cls

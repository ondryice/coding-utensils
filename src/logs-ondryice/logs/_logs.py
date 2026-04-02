from logs._files import STDOUT

class LOGBASE:
  output = STDOUT
  forwarding = False

  @classmethod
  def super (cls) -> None|type[LOGBASE]:
    if cls is LOGBASE:
      return None
    elif issubclass(cls, LOGBASE):
      return cls.__base__
    raise TypeError(f"cannot get super log for {cls.__name__} - not a subclass of log")

  @classmethod
  def push (cls, *values, sep=' ', end='\n', flush=False):
    if not cls.output.blocked:
      cls.output.write(*values, sep=sep, end=end, flush=flush).block()
    if cls.forwarding and cls.super():
      cls.super().push(*values, sep=' ', end='\n', flush=flush)
    